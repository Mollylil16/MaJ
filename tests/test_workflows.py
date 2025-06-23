from odoo.tests import common
from odoo.exceptions import ValidationError
import datetime

class TestWorkflows(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.client = self.env['custom.accounting.client']
        self.fournisseur = self.env['custom.accounting.fournisseur']
        self.commande = self.env['custom.accounting.bon_commande_client']
        self.facture = self.env['custom.accounting.facture_finale']
        self.paiement = self.env['custom.accounting.paiement_client']
        self.user = self.env['res.users']

    def test_commande_workflow(self):
        """Test complet du workflow des commandes"""
        # Création des utilisateurs de test
        comptable = self.user.create({
            'name': 'Test Comptable',
            'login': 'test_comptable',
            'groups_id': [(4, self.env.ref('custom.accounting.group_comptable').id)]
        })
        
        superviseur = self.user.create({
            'name': 'Test Superviseur',
            'login': 'test_superviseur',
            'groups_id': [(4, self.env.ref('custom.accounting.group_superviseur').id)]
        })

        # Création d'un client
        client = self.env['custom.accounting.client'].create({
            'name': 'Test Client',
            'email': 'test@example.com'
        })

        # Création d'une commande en tant que comptable
        self.env = self.env(user=comptable)
        commande = self.commande.create({
            'name': 'BC-001',
            'client_id': client.id,
            'date_commande': datetime.date.today()
        })
        
        # Le comptable ne peut pas approuver
        with self.assertRaises(ValidationError):
            commande.action_approve()

        # Confirmation par le comptable
        commande.action_confirm()
        self.assertEqual(commande.state, 'confirmed')

        # Approbation par le superviseur
        self.env = self.env(user=superviseur)
        commande.action_approve()
        self.assertEqual(commande.state, 'approved')

        # Génération de l'accusé de réception
        commande.action_accuse()
        self.assertEqual(commande.state, 'accuse')

    def test_facture_workflow(self):
        """Test complet du workflow des factures"""
        # Création des utilisateurs de test
        comptable = self.user.create({
            'name': 'Test Comptable',
            'login': 'test_comptable',
            'groups_id': [(4, self.env.ref('custom.accounting.group_comptable').id)]
        })
        
        superviseur = self.user.create({
            'name': 'Test Superviseur',
            'login': 'test_superviseur',
            'groups_id': [(4, self.env.ref('custom.accounting.group_superviseur').id)]
        })

        # Création d'un client
        client = self.env['custom.accounting.client'].create({
            'name': 'Test Client',
            'email': 'test@example.com'
        })

        # Création d'une facture en tant que comptable
        self.env = self.env(user=comptable)
        facture = self.facture.create({
            'name': 'FAC-001',
            'client_id': client.id,
            'date_facture': datetime.date.today()
        })
        
        # Le comptable ne peut pas approuver
        with self.assertRaises(ValidationError):
            facture.action_approve()

        # Confirmation par le comptable
        facture.action_confirm()
        self.assertEqual(facture.state, 'confirmed')

        # Approbation par le superviseur
        self.env = self.env(user=superviseur)
        facture.action_approve()
        self.assertEqual(facture.state, 'approved')

        # Paiement de la facture
        facture.action_pay()
        self.assertEqual(facture.state, 'paid')

    def test_paiement_workflow(self):
        """Test complet du workflow des paiements"""
        # Création des utilisateurs de test
        comptable = self.user.create({
            'name': 'Test Comptable',
            'login': 'test_comptable',
            'groups_id': [(4, self.env.ref('custom.accounting.group_comptable').id)]
        })
        
        superviseur = self.user.create({
            'name': 'Test Superviseur',
            'login': 'test_superviseur',
            'groups_id': [(4, self.env.ref('custom.accounting.group_superviseur').id)]
        })

        # Création d'un client
        client = self.env['custom.accounting.client'].create({
            'name': 'Test Client',
            'email': 'test@example.com'
        })

        # Création d'un paiement en tant que comptable
        self.env = self.env(user=comptable)
        paiement = self.paiement.create({
            'name': 'PAI-001',
            'client_id': client.id,
            'montant': 100.0,
            'date_paiement': datetime.date.today()
        })
        
        # Le comptable ne peut pas approuver
        with self.assertRaises(ValidationError):
            paiement.action_approve()

        # Confirmation par le comptable
        paiement.action_confirm()
        self.assertEqual(paiement.state, 'confirmed')

        # Approbation par le superviseur
        self.env = self.env(user=superviseur)
        paiement.action_approve()
        self.assertEqual(paiement.state, 'approved')

        # Paiement effectué
        paiement.action_pay()
        self.assertEqual(paiement.state, 'paid')
