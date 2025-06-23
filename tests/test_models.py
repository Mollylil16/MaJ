from odoo.tests import common
from odoo.exceptions import ValidationError
import datetime

class TestModels(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.client = self.env['custom.accounting.client']
        self.fournisseur = self.env['custom.accounting.fournisseur']
        self.commande = self.env['custom.accounting.bon_commande_client']
        self.facture = self.env['custom.accounting.facture_finale']
        self.paiement = self.env['custom.accounting.paiement_client']

    def test_client_creation(self):
        """Test de la création d'un client"""
        client = self.client.create({
            'name': 'Test Client',
            'email': 'test@example.com',
            'entreprise_id': self.env['custom.accounting.entreprise'].create({'name': 'Test Entreprise'}).id
        })
        self.assertEqual(client.name, 'Test Client')
        self.assertTrue(client.id)

    def test_fournisseur_creation(self):
        """Test de la création d'un fournisseur"""
        fournisseur = self.fournisseur.create({
            'name': 'Test Fournisseur',
            'email': 'test@example.com',
            'entreprise_id': self.env['custom.accounting.entreprise'].create({'name': 'Test Entreprise'}).id
        })
        self.assertEqual(fournisseur.name, 'Test Fournisseur')
        self.assertTrue(fournisseur.id)

    def test_commande_workflow(self):
        """Test du workflow des commandes"""
        client = self.env['custom.accounting.client'].create({
            'name': 'Test Client',
            'email': 'test@example.com'
        })
        
        commande = self.commande.create({
            'name': 'BC-001',
            'client_id': client.id,
            'date_commande': datetime.date.today()
        })

        # Test du changement d'état
        commande.action_confirm()
        self.assertEqual(commande.state, 'confirmed')
        
        commande.action_approve()
        self.assertEqual(commande.state, 'approved')
        
        commande.action_accuse()
        self.assertEqual(commande.state, 'accuse')

    def test_facture_workflow(self):
        """Test du workflow des factures"""
        client = self.env['custom.accounting.client'].create({
            'name': 'Test Client',
            'email': 'test@example.com'
        })
        
        facture = self.facture.create({
            'name': 'FAC-001',
            'client_id': client.id,
            'date_facture': datetime.date.today()
        })

        # Test du changement d'état
        facture.action_confirm()
        self.assertEqual(facture.state, 'confirmed')
        
        facture.action_approve()
        self.assertEqual(facture.state, 'approved')
        
        facture.action_pay()
        self.assertEqual(facture.state, 'paid')

    def test_paiement_workflow(self):
        """Test du workflow des paiements"""
        client = self.env['custom.accounting.client'].create({
            'name': 'Test Client',
            'email': 'test@example.com'
        })
        
        paiement = self.paiement.create({
            'name': 'PAI-001',
            'client_id': client.id,
            'montant': 100.0,
            'date_paiement': datetime.date.today()
        })

        # Test du changement d'état
        paiement.action_confirm()
        self.assertEqual(paiement.state, 'confirmed')
        
        paiement.action_approve()
        self.assertEqual(paiement.state, 'approved')
        
        paiement.action_pay()
        self.assertEqual(paiement.state, 'paid')

    def test_sequence_generation(self):
        """Test de la génération des séquences"""
        client = self.env['custom.accounting.client'].create({
            'name': 'Test Client',
            'email': 'test@example.com'
        })
        
        # Test des séquences pour les commandes
        commande = self.commande.create({
            'client_id': client.id,
            'date_commande': datetime.date.today()
        })
        self.assertTrue(commande.name.startswith('BC-'))

        # Test des séquences pour les factures
        facture = self.facture.create({
            'client_id': client.id,
            'date_facture': datetime.date.today()
        })
        self.assertTrue(facture.name.startswith('FAC-'))

    def test_constraint_validation(self):
        """Test des contraintes de validation"""
        with self.assertRaises(ValidationError):
            # Test de la contrainte d'unicité des noms de commande
            self.commande.create({
                'name': 'BC-001',
                'client_id': self.env['custom.accounting.client'].create({'name': 'Test Client'}).id
            })
            self.commande.create({
                'name': 'BC-001',
                'client_id': self.env['custom.accounting.client'].create({'name': 'Test Client'}).id
            })

        with self.assertRaises(ValidationError):
            # Test de la contrainte d'unicité des noms de facture
            self.facture.create({
                'name': 'FAC-001',
                'client_id': self.env['custom.accounting.client'].create({'name': 'Test Client'}).id
            })
            self.facture.create({
                'name': 'FAC-001',
                'client_id': self.env['custom.accounting.client'].create({'name': 'Test Client'}).id
            })
