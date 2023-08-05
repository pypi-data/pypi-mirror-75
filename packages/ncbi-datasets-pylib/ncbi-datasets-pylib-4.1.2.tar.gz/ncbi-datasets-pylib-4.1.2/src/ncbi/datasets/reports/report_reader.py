import yaml
import logging

from google.protobuf.json_format import ParseDict, SerializeToJsonError, ParseError

import ncbi.datasets.v1alpha1.reports.virus_pb2 as virus_report_pb2
import ncbi.datasets.v1alpha1.reports.assembly_pb2 as assembly_report_pb2
import ncbi.datasets.v1alpha1.reports.gene_pb2 as gene_report_pb2


logger = logging.getLogger()


class DatasetsReportReader():
    # Load yaml in 'buf' and parse resulting dictionary into protobuf 'schema_pb'
    def _load_and_parse_report(self, buf, schema_pb, from_array=False):
        try:
            report_dict = yaml.safe_load(buf)
            if not report_dict:
                logger.error("Empty report from file")
            try:
                if from_array:
                    ParseDict(report_dict[0], schema_pb, ignore_unknown_fields=False)
                else:
                    ParseDict(report_dict, schema_pb, ignore_unknown_fields=False)
            except (SerializeToJsonError, ParseError) as e:
                logger.error(f"Error converting yaml to schema: {e}")
        except yaml.YAMLError as e:
            logger.error(f"Error while loading yaml: {e}")
        return schema_pb

    # return full assembly report
    def assembly_report_from_file(self, report_file_name):
        schema_pb = assembly_report_pb2.AssemblyDataReport()
        with open(report_file_name) as fh:
            self._load_and_parse_report(fh.read(), schema_pb)
        return schema_pb

    # return full gene report
    def gene_report_from_file(self, report_file_name):
        schema_pb = gene_report_pb2.GeneDescriptors()
        with open(report_file_name) as fh:
            self._load_and_parse_report(fh.read(), schema_pb)
        return schema_pb

    # return VirusAssembly objects one at a time as report file is read from file
    def read_virus_report_from_file(self, report_file_name):
        with open(report_file_name) as fh:
            virus_assm_gen = self.read_virus_report(fh)
            for virus_assm_pb in virus_assm_gen:
                yield virus_assm_pb

    # return full assembly report given a file handle
    def assembly_report(self, report_file_handle):
        return self._load_and_parse_report(report_file_handle, assembly_report_pb2.AssemblyDataReport())

    # return full gene report given a file handle
    def gene_report(self, report_file_handle):
        return self._load_and_parse_report(report_file_handle, gene_report_pb2.GeneDescriptors())

    # rreturn VirusAssembly objects one at a time as report file is read from file handle
    def read_virus_report(self, report_file_handle):
        def _create_assembly_pb(buf):
            schema_pb = virus_report_pb2.VirusAssembly()
            self._load_and_parse_report(buf, schema_pb, from_array=True)
            return schema_pb

        # Ignore header lines up to first '- accession:'
        first_accession = True
        assm_buf = ""
        while True:
            line = report_file_handle.readline()
            if not line:
                yield _create_assembly_pb(assm_buf)
                break
            if isinstance(line, bytes):
                line = line.decode("utf-8")
            # Each line that starts with: '- accession:' is a new asembly
            # and (except for the first such line) the end of the previous one
            if line.startswith('- accession:'):
                if not first_accession:
                    yield _create_assembly_pb(assm_buf)
                first_accession = False
                assm_buf = line
            # Lines other than '- accession' with no identation are not part of an
            # assembly, e.g. the count at the end of the report
            elif line[0] == ' ':
                assm_buf += line
