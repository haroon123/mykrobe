from mykrobe.probes import AlleleGenerator
from mykrobe.variants.schema.models import Variant
from mykrobe.variants.schema.models import VariantSet
from mykrobe.variants.schema.models import Reference
from mykrobe.variants.schema.models import ReferenceSet
from mongoengine import connect
DB = connect('mykrobe-test')


class TestLargeINDELAlleleGenerator():

    def setup(self):
        DB.drop_database('mykrobe-test')
        self.pg = AlleleGenerator(
            reference_filepath="src/mykrobe/data/NC_000962.3.fasta")
        self.reference_set = ReferenceSet().create_and_save(name="ref_set")
        self.variant_set = VariantSet.create_and_save(
            name="this_vcf_file",
            reference_set=self.reference_set)
        self.variant_sets = [self.variant_set]
        self.reference = Reference().create_and_save(
            name="ref",
            md5checksum="sre",
            reference_sets=[
                self.reference_set])

    def test_large_variant(self):
        v = Variant.create(
            variant_sets=self.variant_sets,
            reference=self.reference,
            reference_bases="AACGCCCGGTATCTGAGGATCTGTGTTCTCACCCAATACAAGTCGCATTCACT",
            start=1355983,
            alternate_bases=["ACCGCCCGGTATCTGAGGATTGGTTTTCCACCCAAATACAAGTCGCATTCGCG"])
        panel = self.pg.create(v)
        assert "TCGTCAACGCCCGGTATCTGAGGATCTGTGTTCTCACCCAATACAAGTCGCATTCACTGGACC" in panel.refs
        assert panel.alts == [
            "TCGTCACCGCCCGGTATCTGAGGATTGGTTTTCCACCCAAATACAAGTCGCATTCGCGGGACC"]

    def test_large_variant2(self):
        v = Variant.create(
            variant_sets=self.variant_sets,
            reference=self.reference,
            reference_bases="AACGCCCGGTATCTGAGGATCTGTGTTCTCACCCAATACAAGTCGCATTCAC",
            start=1355983,
            alternate_bases=["ACCGCCCGGTATCTGAGGATTGGTTTTCCACCCAAATACAAGTCGCATTCGC"])
        panel = self.pg.create(v)
        assert "TCGTCAACGCCCGGTATCTGAGGATCTGTGTTCTCACCCAATACAAGTCGCATTCACTGGACC" in panel.refs
        assert panel.alts == [
            "TCGTCACCGCCCGGTATCTGAGGATTGGTTTTCCACCCAAATACAAGTCGCATTCGCTGGACC"]

    def test_large_variant3(self):
        v = Variant.create(
            variant_sets=self.variant_sets,
            reference=self.reference,
            reference_bases="TCGTCAACGCCCGGTATCTGAGGATCTGTGTTCTCACCCAATACAAGTCGCATTCACTGGACC",
            start=1355978,
            alternate_bases=["TCGTCAACGCCCGGTATCTGAGGATCGGTGTTCTCACCCAATACAAGTCGCATTCACTGGACC"])
        panel = self.pg.create(v)
        assert "CAAACCTCGTCAACGCCCGGTATCTGAGGATCTGTGTTCTCACCCAATACAAGTCGCATTCACTGGACCGCCATA" in panel.refs
        assert panel.alts == [
            "CAAACCTCGTCAACGCCCGGTATCTGAGGATCGGTGTTCTCACCCAATACAAGTCGCATTCACTGGACCGCCATA"]

    def test_very_large_variant3(self):
        v = Variant.create(
            variant_sets=self.variant_sets,
            reference=self.reference,
            reference_bases="TCGTCAACGCCCGGTATCTGAGGATCTGTGTTCTCACCCAATACAAGTCGCATTCACTGGACCGCCAT",
            start=1355978,
            alternate_bases=["TCGTCAACGCCCGGTATCTGAGGATCGGTGTTCACCCAATACAAGTCGCATTCACTGGACCGCCAT"])
        panel = self.pg.create(v)
        assert "AAACCTCGTCAACGCCCGGTATCTGAGGATCTGTGTTCTCACCCAATACAAGTCGCATTCACTGGACCGCCATATCTCG" in panel.refs
        assert panel.alts == [
            "CAAACCTCGTCAACGCCCGGTATCTGAGGATCGGTGTTCACCCAATACAAGTCGCATTCACTGGACCGCCATATCTCGC"]

    def test_large_insertion(self):
        v = Variant.create(
            variant_sets=self.variant_sets,
            reference=self.reference,
            reference_bases="C",
            start=2352065,
            alternate_bases=["CCTCGCCTGGGCTGGCGAGCAGACGCAAAATCCCCCGCACGCCCGGCGTGTCGGGGGATTTTGCGTCTG"])
        panel = self.pg.create(v)
        assert "AGCTCGGCCAGCTCAGTCACGTCGCCGCCGCCTCGCCAGTTGACCGCGCCCGCTCGCGGCTAG" in panel.refs
        assert panel.alts == [
            "AAGTCGTCGAGCGAGAACGGTAGTTCCGCGGTGAACCGGTCCAGCTCGGCCAGCTCAGTCACGTCGCCGCCGCCTCGCCTGGGCTGGCGAGCAGACGCAAAATCCCCCGCACGCCCGGCGTGTCGGGGGATTTTGCGTCTGCTCGCCAGTTGACCGCGCCCGCTCGCGGCTAGCGGGCCTACGTGACGTCGTCATGAGATCCGATGACCGATGGC"]

    def test_large_var1(self):
        v = Variant.create(variant_sets=self.variant_sets, reference=self.reference, reference_bases="CGCGGGAGTAGAACGATCGCCAAGTGGTCGGTCTTGGCTGCCCACTTCATCCCCGGCGCCACCGGCAGGTCTCGCGGTCATCTCGACCAACGGAGGGCCGTCGGTGGTTCGTATCCGGCCAAGAACGGCGAGAACGGTTTGTGCCTCTATGCCAGGGTGAATGTCTCATCTCCCAGGCGGACGGTGATATCCAGTTCTCCGCCAAGAGCGGACACGTATTTGCGCAGTGTGTTGACCTGTGCGGAGCCGATGTCGCCGTTCTCGATGCTGGATACCCGGCTCTGCCGGATGTGCGCCAGCGCAGCCACCTGGACCTGGGTGAGTGACTGAGCCGCGCGCAGCTCCCGGAGCCGGAATGCCCGCACTTCATCGCGCATTCGTGCCTTGTGCCGGTCCACCGCCTCCCGGTTAACGGGACGTACGGCGTCCATGTCCCGTAGTGTCATCGCCATCGTGCCACTTACCCTTTCTTGCGCTTGCGCCTCTTTGGCTTCGTGTCCTCGAACTGTGCGAGATGTTCGGCAAACATCTCATCGGCCGCTTTGATCTTCTCGTCGTACCACTGGGTCCACCGCCCGGCCTTGTTACCGGCGGCCAGCATGATCGCCTGCCGCGCCGGGTCGAAGGCGAACAGAATGCGGACCTCGGACCGCCCTTGTGATCCTGGACGCAGCTCCTTCATGTTCTTGTGGCGCGACCCACGCACCGTGTCCACCAGAGGACAGCCAAGTGCGGGGCCCTCTTCCTCGAGAACCTCGATAGCTGCGAACACCAATTCGTAGGTCTCTCGGTCCAAGCCGTTGAGCCAGGCGGAGATGCGCTCCACATCCGCCGTCCACCCCACAGAGTCGCAGAGTAGCGCGATACGCGATATCACACAAGGGTGATATTCCTCCGGGTAAGAGCAGCGGGCGACGGGGCTACCGTCGAGGAAATGCCGGCAGGCGAGGACGGACTCTGCGCACCCGGGCCGTTGAAACAGTAGCCTGTGCCAGGCCGAGAATTCATCCCCACGTATGAGGCAGTACAGTGCGCCGCCGTGCGCGTTCTCCCATGGAACGTTCACGGGCTCCCGTGGATGACAGGCGTTTCATGAACGCCAGCGCCGCCGCAACCCGACCGAAAGCGGTTGACCCCAAGGAGAGCTGGAAGTCGAGGCCACCACCTTCGCCGCGGAGTTGCTCATGCCCGAGAGCGAGACTCGTCCCGAAATACGCCGGCTCGATTTCGGCAAGTTGCTCGAACTGAAGCGGGAATGGGCGTCGACCCGCTCGACCAGCCCCAGCCGGGTGACCAGCCCCAGCCGGGTGACCAGCCGATGCACCGCGGCGATCCCACCGAAGCCGGTGGCATCGATGTTGGCGCCGACCTCGTAGCGCACCGCGCCCGAACCCAGCATCGGCCTGGGCTGCGCCGCCCAGCGTCCAGCCCGCGCGTGCCGCGCCGCCACCCTGCGCCCTCGGCGTGTGATGTTTCGCCGACTCTGTTCATGGGTTATCTTCTTCACCACAAAGGCCTTTCCTGCTGGGCTGTGTTGAGGTCGCAAACCCAGCCAGGGTAAGGCCTTTGGCCTCTCCTACCCGGCCGACACGCTTACTGAAGGCCTAGTCTAGGCAGGCCATTCAATCTGCGGAATCGAAAAATTCGGTTCCAGCCTGCTCGTTTCCTTTCCGACAGCGATCTGACGTTGCGTAACGTCATTTGTACGGACTCTTTTAGCGGCATTGATTTCAGATGCCAACGCCGTCTGTGCTGTAGCGCCGATTGGCCGAAACTGTAAATTTGTATGATTATTTAAATCTTTGACGAACACGCGCCACAAACGTACTATCTCTTTGGCAAAGTCCACCGGCATCTCATTCAACGGTTTTGTTTGCGCGTGGTCGTCATATGTTGGTAACTGTGTAACCGGCCGCCTATCTTGCGCGTGCATCATATGACTATGAATCGGCCTTCTCCAGTGAAATTGATACAAGATCGATCCGATAAGCGGTACCTTGTACACAGTGCAATTGTAGTAATTCGCGTTTTGTCCTACGCTTGTATTCTGCGTGAAGAATTCA", start=2266659, alternate_bases=[
            "CACGCGAGTTGTAGATGATCGTTGAGTGGTCTTGCTTGGACTTCCATTTCATCTTTTCGACGCGCCAGGTCTCGCGGTCCTCCGGATCTGCGCCCGGTTTGAGTTGCACATCAAGGGGATACGGCTTGACCGACTCGTAGCCGACATGTAAGTCGGCTAGTTTCCGGCCGGCGCTGGCGAGCTGGTCGAAGCGTTCGCGGGTCTCCGGTGTTGGGATGTGCGGGAGCATCTTCTTGAGGTCAGCGGCGTATTTTGTGCGGTAGGCGGGGTCATGCAGCAGGCCGTAGACGTAGTAGAAGATGTCGTCTTTGGTGACTTGGTCGCCGATCGTGTCGCGGTAGAGCTTGAGGATGACGCCGGTGATGTTGTCGACGCGGCGGTAGCCGTGGTCGTCTACTTCGGCGTTGGTGGTGGACTCGAAATCGAGTTCGCCGTCACGTGGTTCGGTCTTCTCGTAGGTCCAGCGCGGGAAGAATTGACCGTTGCTTGAGCCCCAGAATGCGAGATCGGGGATAGCGTTTAGCATCAGACACGAGAAGGGCTTGTCTGAGCCCATGCCAACCACGTAGTAACCGACATTCCCGTGCTCCGGCGTCGGAAACATCGACGGAAGCTGGTAGGTACAGTTGTTGAGCTGCTGGTTGGGGTCGAGGTAGGCGTGCTCTTTCGTAAATGGTCGGTACGTGCCGAGCCGCATTCCCGCGGGAGCGAATTCGATGCGAATGCCTTGTGCCACTTGCCGCTTGTTGATGCGGTCCCAGCTGAACTTGGCCGAGTCCACGGTAATGAGGGCGTCAACCGGCGGGGTCTTGGCGTCCCTTCCGCGGATCTCGTTGATCCGGTCGACCTCCGAGTTGTAGAAGTCGATCGTGCGTCCGATGTTGGCCTCGAGCGCACCACGTGAAAAGTTGTAACACCACGCATCCCGGCTGGTCTTCAAGCCCGCGGAATAGTTCGCGAAGACACGTGTCACGTCAAGAGCAGCCTTCTTGTCGCCGATAACCGGCCACGCGCTGAACGCGTCGTCGCGTTGGTTGACCCAGTCACCGTGCAAGTTGGGTGTGACTGTCTGCCATTCCACCGTGTCGAGGTAGCCGTCGCCGACGATCCGCAACTTCTCCTCGCGACTCAGGTAATCGCCGATGTCGCGGTAAAGGACATCGCATGGCCCGCTGTGCTTCGGATCCTTGATGCCAAGGAAGATCGCCACCGTGTTGCGACTCCCCCCGCCAAAGACCTTGCCGCCTTCCTGGCGTGAGAGTTCCCCAGCTGTGCGCTGGTTCCCCCGCAGGTTGTACACATATACCGCCGCGTAGTCGTCGGCGAGCGACAACCGCATGCCGTCTGCCGTGTTGCCGTCTATGTACCCACCATTGGAGACGAATCCGACAACACCGTTGTCACCAATGCGGTCGGTCGCCCACCGGAACGCGCGAATATACGAGTCGTACAGGCTGTTCTTCAGCTGCGCCGTCGACCGCTTCGCGTACGTCTGCTCAATCCGCCCGTCCAACGTCGGATACTTCACGTTGGCGTTCAGGTCGTTCGCGCTGCTCTGCCCCACCGAGTACGGCGGATTCCCGATGATCACGCTGATCGGCGTCGCCAGCTGTCGCAAGATCCGAGCGTTGTTGTACGGGAACATGATCGCGTCCATCGAGTCCCCGGCTTCGGAAATCTGGAACGTGTCGGCCAGCGCCATCCCGGGGAACGGCTCATAGGCGTCGGCGTCGGCGGTCTTGCCCGCCAAAGCATGGTAGGTCGACTCGATGTTCACCGCGGCGATGTAGTACGCCAGCAGCATGATCTCGTTGGCGTGCAGCTCTTGCGAGTACTTTCGGGTGAGGTCGGCGGCCGTGATCAGGTCGGACTGCAGCAGCCGGGTAATGAATGTGCCCGTCCCGGCGAAGCCGTCCAGAATATGCACGCCCTCGTCGGTCAGCCCGCGCCCGAAATGCTTGCGCGACACGAAATCAGCCGCCCGCACAATGAAGTCCACGACCTCGACCGGCGTGTACACGATCCCCAGCGCCTCGGCCTGCTTCTTGAAGCCGATGCGGAAGAACTTCTCGTACAGCTCGGCGATCACCTGCTGCTTGCCCTCGGCGCTGGTGACCTCGCCGGCGCGCCGTCGCACCGATTCGTAAAAGCCTTCCAACCGAGCGGTTTCGGCCTCCAGGCCGGCACCCCCGACGGTGTCGACCATCTTCTGCATGGCCCGCGACACCGGGTTGTGCGACGCGAAGTCATGCCCGGCGAACAGCGCGTCGAACACCGGCTTGGTGATCAGGTGCTGCGAGAGCATGCTGATCGCGTCATCGGGGGTGATCGAGTCATTGAGGTTATCGCGCAGCCCGGCCAGGAACTGCTCGAACGCCGCCGCCGCCGTAGCGTCGGCGCCGCCGAGCAGGGCGTGGATACGGGTGGTCAGCGTCGCGGCGATGTCGGCGACATCGGCGGCCCACTGCTCCCAATAGGTCCGGGTGCCAACCTTGTCGACGATGCGCGCGTAGATCGCTTCCTGCCACTGCGACAACGAGAACATCGCCAACTGCTCCGCGACGGCGGGTCCCGCCTCGTCGGAGGTCGGCCCGATGTGACCGCCCAACAGCTTGTCGCTGCCTTCACCGGTCTTCGTCGGCTTCACGTTCAGCGCAATGCTGTTCACCATCGCGTCGAAGCGCTCGTCGTGCGACCGCAACGCGTTGAGGACCTGCCACACCACCTTGAACCGTTTGTTGTCGGCCAACGCGGCAGACGGCTCGACACCCTCGGGCACCGCCACCGGCAAGATGACGTACCCGTAGTCCTTGCCGGGCGACTTGCGCATCACCCGACCGACCGACTGCACCACGTCGACGATGGAATTGCGCGGATTCAGGAACAGCACCGCGTCCAGCGCGGGCACGTCGACCCCTTCGGAGAGGCAGCGGGCGTTGGACAGGATGCGGCATTCATCCTCGGCGACCACGCCTTTGAGCCAGGCCAGCTGTTCGTTGCGGACCAGCGCGTTGAACGTCCCGTCCACGTGGCGCACCG"])
        panel = self.pg.create(v)
        assert "TGGTGACGCGGGAGTAGAACGATCGCCAAGTGGTCGGTCTTGGCTGCCCACTTCATCCCCGGCGCCACCGGCAGGTCTCGCGGTCATCTCGACCAACGGAGGGCCGTCGGTGGTTCGTATCCGGCCAAGAACGGCGAGAACGGTTTGTGCCTCTATGCCAGGGTGAATGTCTCATCTCCCAGGCGGACGGTGATATCCAGTTCTCCGCCAAGAGCGGACACGTATTTGCGCAGTGTGTTGACCTGTGCGGAGCCGATGTCGCCGTTCTCGATGCTGGATACCCGGCTCTGCCGGATGTGCGCCAGCGCAGCCACCTGGACCTGGGTGAGTGACTGAGCCGCGCGCAGCTCCCGGAGCCGGAATGCCCGCACTTCATCGCGCATTCGTGCCTTGTGCCGGTCCACCGCCTCCCGGTTAACGGGACGTACGGCGTCCATGTCCCGTAGTGTCATCGCCATCGTGCCACTTACCCTTTCTTGCGCTTGCGCCTCTTTGGCTTCGTGTCCTCGAACTGTGCGAGATGTTCGGCAAACATCTCATCGGCCGCTTTGATCTTCTCGTCGTACCACTGGGTCCACCGCCCGGCCTTGTTACCGGCGGCCAGCATGATCGCCTGCCGCGCCGGGTCGAAGGCGAACAGAATGCGGACCTCGGACCGCCCTTGTGATCCTGGACGCAGCTCCTTCATGTTCTTGTGGCGCGACCCACGCACCGTGTCCACCAGAGGACAGCCAAGTGCGGGGCCCTCTTCCTCGAGAACCTCGATAGCTGCGAACACCAATTCGTAGGTCTCTCGGTCCAAGCCGTTGAGCCAGGCGGAGATGCGCTCCACATCCGCCGTCCACCCCACAGAGTCGCAGAGTAGCGCGATACGCGATATCACACAAGGGTGATATTCCTCCGGGTAAGAGCAGCGGGCGACGGGGCTACCGTCGAGGAAATGCCGGCAGGCGAGGACGGACTCTGCGCACCCGGGCCGTTGAAACAGTAGCCTGTGCCAGGCCGAGAATTCATCCCCACGTATGAGGCAGTACAGTGCGCCGCCGTGCGCGTTCTCCCATGGAACGTTCACGGGCTCCCGTGGATGACAGGCGTTTCATGAACGCCAGCGCCGCCGCAACCCGACCGAAAGCGGTTGACCCCAAGGAGAGCTGGAAGTCGAGGCCACCACCTTCGCCGCGGAGTTGCTCATGCCCGAGAGCGAGACTCGTCCCGAAATACGCCGGCTCGATTTCGGCAAGTTGCTCGAACTGAAGCGGGAATGGGCGTCGACCCGCTCGACCAGCCCCAGCCGGGTGACCAGCCCCAGCCGGGTGACCAGCCGATGCACCGCGGCGATCCCACCGAAGCCGGTGGCATCGATGTTGGCGCCGACCTCGTAGCGCACCGCGCCCGAACCCAGCATCGGCCTGGGCTGCGCCGCCCAGCGTCCAGCCCGCGCGTGCCGCGCCGCCACCCTGCGCCCTCGGCGTGTGATGTTTCGCCGACTCTGTTCATGGGTTATCTTCTTCACCACAAAGGCCTTTCCTGCTGGGCTGTGTTGAGGTCGCAAACCCAGCCAGGGTAAGGCCTTTGGCCTCTCCTACCCGGCCGACACGCTTACTGAAGGCCTAGTCTAGGCAGGCCATTCAATCTGCGGAATCGAAAAATTCGGTTCCAGCCTGCTCGTTTCCTTTCCGACAGCGATCTGACGTTGCGTAACGTCATTTGTACGGACTCTTTTAGCGGCATTGATTTCAGATGCCAACGCCGTCTGTGCTGTAGCGCCGATTGGCCGAAACTGTAAATTTGTATGATTATTTAAATCTTTGACGAACACGCGCCACAAACGTACTATCTCTTTGGCAAAGTCCACCGGCATCTCATTCAACGGTTTTGTTTGCGCGTGGTCGTCATATGTTGGTAACTGTGTAACCGGCCGCCTATCTTGCGCGTGCATCATATGACTATGAATCGGCCTTCTCCAGTGAAATTGATACAAGATCGATCCGATAAGCGGTACCTTGTACACAGTGCAATTGTAGTAATTCGCGTTTTGTCCTACGCTTGTATTCTGCGTGAAGAATTCAAACACG" in panel.refs
        assert panel.alts == [
            "GACCGCCGAGTGCGGCTGGATTGGATTTCACAAGGATGCCAATATCCGGCGCAACGCCGTCGAGCGACGGACGGTGCTCGACACGGGAGCCCGGCTATTCTGTGTGCCGCGGGCCGACATCCTGGCAGAGCAAGTCGCGGCACGGTATATTGCGTCCCTTGCGGCGATTGCCCGTGCCGCACGATTTCCGGGACCATTCATCTACACGGTTCACCCGAGCAAGATCGTTCGCGTGCTCTAGTCGTTCATCGCTCCGTTAACCGCCGGCGAGGCCGTCGACGATCTTCATGGTCTCGACGCTGACGGTGGTCACCTTCTTGATGAGGTCGACGATGTAGGTGGGATCGTCGTGTTCGTCGCACCAGTCGTTGGGGTCGTTGACGATGCCCGACGCTTTGTCGGTGGTGACGCGGTAGCGCTCGATGATCCAGCCGAGCGCCGAGCGGGAGCGAGCAGGTAGCGCTCGGCCTCGTCGGGAATGCCGGCGATGGTGACACGCGAGTTGTAGATGATCGTTGAGTGGTCTTGCTTGGACTTCCATTTCATCTTTTCGACGCGCCAGGTCTCGCGGTCCTCCGGATCTGCGCCCGGTTTGAGTTGCACATCAAGGGGATACGGCTTGACCGACTCGTAGCCGACATGTAAGTCGGCTAGTTTCCGGCCGGCGCTGGCGAGCTGGTCGAAGCGTTCGCGGGTCTCCGGTGTTGGGATGTGCGGGAGCATCTTCTTGAGGTCAGCGGCGTATTTTGTGCGGTAGGCGGGGTCATGCAGCAGGCCGTAGACGTAGTAGAAGATGTCGTCTTTGGTGACTTGGTCGCCGATCGTGTCGCGGTAGAGCTTGAGGATGACGCCGGTGATGTTGTCGACGCGGCGGTAGCCGTGGTCGTCTACTTCGGCGTTGGTGGTGGACTCGAAATCGAGTTCGCCGTCACGTGGTTCGGTCTTCTCGTAGGTCCAGCGCGGGAAGAATTGACCGTTGCTTGAGCCCCAGAATGCGAGATCGGGGATAGCGTTTAGCATCAGACACGAGAAGGGCTTGTCTGAGCCCATGCCAACCACGTAGTAACCGACATTCCCGTGCTCCGGCGTCGGAAACATCGACGGAAGCTGGTAGGTACAGTTGTTGAGCTGCTGGTTGGGGTCGAGGTAGGCGTGCTCTTTCGTAAATGGTCGGTACGTGCCGAGCCGCATTCCCGCGGGAGCGAATTCGATGCGAATGCCTTGTGCCACTTGCCGCTTGTTGATGCGGTCCCAGCTGAACTTGGCCGAGTCCACGGTAATGAGGGCGTCAACCGGCGGGGTCTTGGCGTCCCTTCCGCGGATCTCGTTGATCCGGTCGACCTCCGAGTTGTAGAAGTCGATCGTGCGTCCGATGTTGGCCTCGAGCGCACCACGTGAAAAGTTGTAACACCACGCATCCCGGCTGGTCTTCAAGCCCGCGGAATAGTTCGCGAAGACACGTGTCACGTCAAGAGCAGCCTTCTTGTCGCCGATAACCGGCCACGCGCTGAACGCGTCGTCGCGTTGGTTGACCCAGTCACCGTGCAAGTTGGGTGTGACTGTCTGCCATTCCACCGTGTCGAGGTAGCCGTCGCCGACGATCCGCAACTTCTCCTCGCGACTCAGGTAATCGCCGATGTCGCGGTAAAGGACATCGCATGGCCCGCTGTGCTTCGGATCCTTGATGCCAAGGAAGATCGCCACCGTGTTGCGACTCCCCCCGCCAAAGACCTTGCCGCCTTCCTGGCGTGAGAGTTCCCCAGCTGTGCGCTGGTTCCCCCGCAGGTTGTACACATATACCGCCGCGTAGTCGTCGGCGAGCGACAACCGCATGCCGTCTGCCGTGTTGCCGTCTATGTACCCACCATTGGAGACGAATCCGACAACACCGTTGTCACCAATGCGGTCGGTCGCCCACCGGAACGCGCGAATATACGAGTCGTACAGGCTGTTCTTCAGCTGCGCCGTCGACCGCTTCGCGTACGTCTGCTCAATCCGCCCGTCCAACGTCGGATACTTCACGTTGGCGTTCAGGTCGTTCGCGCTGCTCTGCCCCACCGAGTACGGCGGATTCCCGATGATCACGCTGATCGGCGTCGCCAGCTGTCGCAAGATCCGAGCGTTGTTGTACGGGAACATGATCGCGTCCATCGAGTCCCCGGCTTCGGAAATCTGGAACGTGTCGGCCAGCGCCATCCCGGGGAACGGCTCATAGGCGTCGGCGTCGGCGGTCTTGCCCGCCAAAGCATGGTAGGTCGACTCGATGTTCACCGCGGCGATGTAGTACGCCAGCAGCATGATCTCGTTGGCGTGCAGCTCTTGCGAGTACTTTCGGGTGAGGTCGGCGGCCGTGATCAGGTCGGACTGCAGCAGCCGGGTAATGAATGTGCCCGTCCCGGCGAAGCCGTCCAGAATATGCACGCCCTCGTCGGTCAGCCCGCGCCCGAAATGCTTGCGCGACACGAAATCAGCCGCCCGCACAATGAAGTCCACGACCTCGACCGGCGTGTACACGATCCCCAGCGCCTCGGCCTGCTTCTTGAAGCCGATGCGGAAGAACTTCTCGTACAGCTCGGCGATCACCTGCTGCTTGCCCTCGGCGCTGGTGACCTCGCCGGCGCGCCGTCGCACCGATTCGTAAAAGCCTTCCAACCGAGCGGTTTCGGCCTCCAGGCCGGCACCCCCGACGGTGTCGACCATCTTCTGCATGGCCCGCGACACCGGGTTGTGCGACGCGAAGTCATGCCCGGCGAACAGCGCGTCGAACACCGGCTTGGTGATCAGGTGCTGCGAGAGCATGCTGATCGCGTCATCGGGGGTGATCGAGTCATTGAGGTTATCGCGCAGCCCGGCCAGGAACTGCTCGAACGCCGCCGCCGCCGTAGCGTCGGCGCCGCCGAGCAGGGCGTGGATACGGGTGGTCAGCGTCGCGGCGATGTCGGCGACATCGGCGGCCCACTGCTCCCAATAGGTCCGGGTGCCAACCTTGTCGACGATGCGCGCGTAGATCGCTTCCTGCCACTGCGACAACGAGAACATCGCCAACTGCTCCGCGACGGCGGGTCCCGCCTCGTCGGAGGTCGGCCCGATGTGACCGCCCAACAGCTTGTCGCTGCCTTCACCGGTCTTCGTCGGCTTCACGTTCAGCGCAATGCTGTTCACCATCGCGTCGAAGCGCTCGTCGTGCGACCGCAACGCGTTGAGGACCTGCCACACCACCTTGAACCGTTTGTTGTCGGCCAACGCGGCAGACGGCTCGACACCCTCGGGCACCGCCACCGGCAAGATGACGTACCCGTAGTCCTTGCCGGGCGACTTGCGCATCACCCGACCGACCGACTGCACCACGTCGACGATGGAATTGCGCGGATTCAGGAACAGCACCGCGTCCAGCGCGGGCACGTCGACCCCTTCGGAGAGGCAGCGGGCGTTGGACAGGATGCGGCATTCATCCTCGGCGACCACGCCTTTGAGCCAGGCCAGCTGTTCGTTGCGGACCAGCGCGTTGAACGTCCCGTCCACGTGGCGCACCGAACACGCCAGGCCCGGGCCGTCGTCAACCAATTCGCGGTATGCCTCAACCACTTTCGGGAACAGCTCGGCAACCTGCTTGGACGTCTTGATGTCCTTGGCGAACGCCACCGCCCGACGCATCGGCGGCTCACCGGCGACAATGCCGGTACCGGACCGCTTGGCCAGGCCATTCCAGCAGCCGACGATCTTGGAGGCGTCGTCGAGCATCAGCTCGCCGGAAACCCCGGAGAGTTCCTGCTGCAACCGGGGCGCGATCACGCCCTGATCGACGGTGAGCACCATCACCTTGTAGTCGGTGAGCAGCCCGCGCTCCACCGCCTCGCCGAACGACAGCCGGTGAAACTCCGGCCCGAACGTCAGCTCGTCGTCCATCGACACCAACTCGGCGGAGTGCTGGTCGGCCCTGTCCTTGATGCTCTCGGTGAAAATCCTTGGCGTGGCGGTCATATACAGCCGCCGGGCCGCCTTCAGATACTGACCGTCGTGCACCCGC"]
