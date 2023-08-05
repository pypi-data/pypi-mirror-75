# -*- coding: utf-8 -*-
"""Module containing the DOV data type for CPT measurements (Sonderingen),
including subtypes."""
from pydov.types.abstract import AbstractDovSubType, AbstractDovType
from pydov.types.fields import WfsField, XmlField


class Meetdata(AbstractDovSubType):

    rootpath = './/sondering/sondeonderzoek/penetratietest/meetdata'

    fields = [
        XmlField(name='z',
                 source_xpath='/sondeerdiepte',
                 definition='Diepte waarop sondeerparameters geregistreerd '
                            'werden, uitgedrukt in meter ten opzicht van het '
                            'aanvangspeil.',
                 datatype='float'),
        XmlField(name='qc',
                 source_xpath='/qc',
                 definition='Opgemeten waarde van de conusweerstand, '
                            'uitgedrukt in MPa.',
                 datatype='float'),
        XmlField(name='Qt',
                 source_xpath='/Qt',
                 definition='Opgemeten waarde van de totale weerstand, '
                            'uitgedrukt in kN.',
                 datatype='float'),
        XmlField(name='fs',
                 source_xpath='/fs',
                 definition='Opgemeten waarde van de plaatelijke '
                            'kleefweerstand, uitgedrukt in kPa.',
                 datatype='float'),
        XmlField(name='u',
                 source_xpath='/u',
                 definition='Opgemeten waarde van de porienwaterspanning, '
                            'uitgedrukt in kPa.',
                 datatype='float'),
        XmlField(name='i',
                 source_xpath='/i',
                 definition='Opgemeten waarde van de inclinatie, uitgedrukt '
                            'in graden.',
                 datatype='float')
    ]


class Sondering(AbstractDovType):
    """Class representing the DOV data type for CPT measurements."""

    subtypes = [Meetdata]

    fields = [
        WfsField(name='pkey_sondering', source_field='fiche',
                 datatype='string'),
        WfsField(name='sondeernummer', source_field='sondeernummer',
                 datatype='string'),
        WfsField(name='x', source_field='X_mL72', datatype='float'),
        WfsField(name='y', source_field='Y_mL72', datatype='float'),
        WfsField(name='start_sondering_mtaw', source_field='Z_mTAW',
                 datatype='float'),
        WfsField(name='diepte_sondering_van', source_field='diepte_van_m',
                 datatype='float'),
        WfsField(name='diepte_sondering_tot', source_field='diepte_tot_m',
                 datatype='float'),
        WfsField(name='datum_aanvang', source_field='datum_aanvang',
                 datatype='date'),
        WfsField(name='uitvoerder', source_field='uitvoerder',
                 datatype='string'),
        WfsField(name='sondeermethode', source_field='sondeermethode',
                 datatype='string'),
        WfsField(name='apparaat', source_field='apparaat_type',
                 datatype='string'),
        XmlField(name='datum_gw_meting',
                 source_xpath='/sondering/visueelonderzoek/'
                              'datumtijd_waarneming_grondwaterstand',
                 definition='Datum en tijdstip van waarneming van de '
                            'grondwaterstand.',
                 datatype='datetime'),
        XmlField(name='diepte_gw_m',
                 source_xpath='/sondering/visueelonderzoek/grondwaterstand',
                 definition='Diepte water in meter ten opzicht van het '
                            'aanvangspeil.',
                 datatype='float')
    ]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Sondering (CPT measurement), being a URI of
            the form `https://www.dov.vlaanderen.be/data/sondering/<id>`.

        """
        super(Sondering, self).__init__('sondering', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        s = cls(feature.findtext('./{{{}}}fiche'.format(namespace)))

        for field in cls.get_fields(source=('wfs',)).values():
            s.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return s
