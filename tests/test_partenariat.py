from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestPartenariat(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Partenariat = self.env['gestion_comptable_sfec.partenariat']
        self.Facture = self.env['gestion_comptable_sfec.facture_finale']
        
    def test_create_partenariat(self):
        """Test la création d'un partenariat"""
        partenariat = self.Partenariat.create({
            'name': 'Test Partenariat',
            'type_partenariat': 'spirax',
            'date_debut': '2023-01-01',
            'date_fin': '2024-12-31',
            'conditions': 'Conditions de test'
        })
        self.assertEqual(partenariat.name, 'Test Partenariat')
        self.assertEqual(partenariat.type_partenariat, 'spirax')

    def test_validation_dates(self):
        """Test la validation des dates"""
        with self.assertRaises(ValidationError):
            self.Partenariat.create({
                'name': 'Test Partenariat',
                'type_partenariat': 'spirax',
                'date_debut': '2024-01-01',
                'date_fin': '2023-12-31',
                'conditions': 'Conditions de test'
            })

    def test_facture_validation(self):
        """Test la validation des factures"""
        facture = self.Facture.create({
            'statut': 'en_attente',
            'montant_total': 1000.00
        })
        facture.statut = 'valide'
        self.assertEqual(facture.statut, 'valide')

    def test_facture_paiement(self):
        """Test le processus de paiement"""
        facture = self.Facture.create({
            'statut': 'en_attente',
            'montant_total': 1000.00
        })
        facture.statut = 'payee'
        self.assertEqual(facture.statut, 'payee')
        self.assertIsNotNone(facture.date_paiement)

    def test_partenariat_expiration(self):
        """Test l'expiration des partenariats"""
        partenariat = self.Partenariat.create({
            'name': 'Test Partenariat',
            'type_partenariat': 'spirax',
            'date_debut': '2023-01-01',
            'date_fin': '2023-06-01',
            'conditions': 'Conditions de test'
        })
        with self.assertRaises(ValidationError):
            partenariat._validate_partenariat()
