import pytest
from tenacity import RetryError

import time
import pandas as pd
from . import DEV_URL
from DNA_analyser_IBP.callers import (
    FileSequenceFactory,
    NCBISequenceFactory,
    SequenceModel,
    SequenceMethods,
    TextSequenceFactory,
    User
)


@pytest.fixture(scope="module")
def user():
    return User(email="user@mendelu.cz", password="user", server=DEV_URL)


@pytest.fixture(scope="module")
def host():
    return User(email="host", password="host", server=DEV_URL)


@pytest.fixture(scope="module")
def sequence():
    return SequenceModel(
        id="some_random_id",
        name="NC_006591.3 Canis lupus familiaris breed boxer chromosome 9",
        created="c",
        type="t",
        circular="cr",
        length=100,
        ncbi="NCB",
        tags=["ss"],
        fastaComment=None,
        nucleicCounts=None,
    )


class TestSequence:

    def test_sequence_creation_and_retrieving_data_frame(self, user):
        """It should create sequence object + test pandas dataframe creation."""

        sequence = SequenceModel(
            id="987acc67-5714-47b1-b56f-1dc56ded7c87",
            name="n",
            created="c",
            type="t",
            circular="cr",
            length=100,
            ncbi="NCB",
            tags=["ss"],
            fastaComment=None,
            nucleicCounts=None,
        )
        assert isinstance(sequence, SequenceModel)
        data_frame = sequence.get_dataframe()
        assert isinstance(data_frame, pd.DataFrame)
        assert data_frame["id"][0] is "987acc67-5714-47b1-b56f-1dc56ded7c87"
        assert data_frame["length"][0] == 100
        assert data_frame["fasta_comment"][0] is None

    def test_sequence_text_creation_and_deleting(self, host):
        """It should create sequence from RAW text + then deletes it."""

        factory = TextSequenceFactory(user=host,
                                      circular=True,
                                      data="ATTCGTTTAGGG",
                                      name="Test",
                                      tags=["testovaci", "test"],
                                      nucleic_type="DNA")
        text_sequence = factory.sequence
        assert isinstance(text_sequence, SequenceModel)
        assert text_sequence.name == "Test"
        time.sleep(2)
        res = SequenceMethods.delete(user=host, id=text_sequence.id)
        assert res is True

    def test_sequence_ncbi_creation_and_deleting(self, host):
        """It should create sequence from RAW text + then deletes it."""

        factory = NCBISequenceFactory(user=host,
                                      circular=True,
                                      name="Theobroma cacao chloroplast",
                                      tags=["Theobroma", "cacao"],
                                      ncbi_id="NC_014676.2")
        ncbi_sequence = factory.sequence
        assert isinstance(ncbi_sequence, SequenceModel)
        assert ncbi_sequence.name == "Theobroma cacao chloroplast"
        time.sleep(2)
        res = SequenceMethods.delete(user=host, id=ncbi_sequence.id)
        assert res is True

    @pytest.mark.skip(reason="Have no file in gitlab pipeline to upload")
    def test_sequence_file_uploading_creation_and_deleting(self, host):
        """It should create sequence from FASTA file + then deletes it."""

        factory = FileSequenceFactory(user=host,
                                      circular=True,
                                      file_path="/home/patrikkaura/Git/DNA_analyser_IBP/tests/sequence.txt",
                                      name="Saccharomyces cerevisiae",
                                      tags=["Saccharomyces"],
                                      sequence_type="DNA",
                                      format="FASTA")
        file_sequence = factory.sequence
        assert isinstance(file_sequence, SequenceModel)
        assert file_sequence.name == "Saccharomyces cerevisiae"
        time.sleep(2)
        res = SequenceMethods.delete(user=host, id=file_sequence.id)
        assert res is True

    def test_sequence_fail_delete(self, host, sequence):
        """It should test deleting non existing sequence."""

        res = SequenceMethods.delete(user=host, id=sequence.id)
        assert res is False

    def test_load_all_sequence_filtered(self, user):
        """It should test loading filtered list of all sequences."""

        sq_lst = [se for se in SequenceMethods.load_all(user=user, tags=[""])]
        assert isinstance(sq_lst[0], SequenceModel)

    def test_load_sequence_by_id(self, user):
        """It should return same object as first object in load all sequence."""

        sq_lst = [se for se in SequenceMethods.load_all(user, tags=[""])]
        test_sequence = sq_lst[0]
        compare_sequence = SequenceMethods.load_by_id(
            user, id=test_sequence.id)
        assert isinstance(test_sequence, SequenceModel)
        assert test_sequence.id == compare_sequence.id

    def test_load_sequence_by_wrong_id(self, user):
        """It should return exception for loading sequence with shitty id."""

        with pytest.raises(Exception):
            SequenceMethods.load_by_id(user, id="random_id")

    def test_loading_sequence_data(self, user):
        """It should return data of given sequence."""

        sq_lst = [se for se in SequenceMethods.load_all(user=user, tags=[""])]
        data = SequenceMethods.load_data(
            user, id=sq_lst[0].id, length=100, possiotion=0, sequence_length=2000)
        assert isinstance(data, str)
        assert len(data) == 100
        # time.sleep(1)

    def test_load_all_sequence_not_filtered(self, user):
        """It should test loading list of all sequences."""

        sq_lst = [se for se in SequenceMethods.load_all(user, tags=[])]
        assert isinstance(sq_lst[0], SequenceModel)

    def test_sequence_factory_for_wrong_server(self, user, sequence):
        """It should test raising connection error for wrong server"""
        usr = user
        usr.server = "http://some_html_bullshit.cz"

        with pytest.raises(Exception):
            _ = TextSequenceFactory(user=usr,
                                    circular=True,
                                    data="ATTCGTTTAGGG",
                                    name="Test",
                                    tags=["testovaci", "test"],
                                    nucleic_type="DNA")
