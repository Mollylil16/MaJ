# Documentation Technique - API Reference

## Structure du Module

### Modèles Principaux

#### PartenariatExclusif
```python
class PartenariatExclusif(models.Model):
    _name = 'gestion_comptable_sfec.partenariat'
    _description = 'Gestion des partenariats exclusifs'

    name = fields.Char('Nom du Partenaire')
    type_partenariat = fields.Selection([
        ('spirax', 'SPIRAX SARCO'),
        ('aprotech', 'APPROTECH')
    ], string='Type de Partenariat')
    date_debut = fields.Date('Date de Début')
    date_fin = fields.Date('Date de Fin')
    conditions = fields.Text('Conditions Particulières')
    active = fields.Boolean('Actif', default=True)
```

#### FactureFinale
```python
class FactureFinale(models.Model):
    _name = 'gestion_comptable_sfec.facture_finale'
    _inherit = 'account.move'

    statut = fields.Selection([
        ('en_attente', 'En Attente'),
        ('valide', 'Validée'),
        ('payee', 'Payée')
    ], string='Statut')
    montant_total = fields.Monetary('Montant Total')
    date_paiement = fields.Date('Date de Paiement')
```

## Sécurité

### Groupes d'Utilisateurs
```xml
<record id="group_gestionnaire" model="res.groups">
    <field name="name">Gestionnaire Comptable</field>
    <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
</record>

<record id="group_admin" model="res.groups">
    <field name="name">Administrateur Comptable</field>
    <field name="implied_ids" eval="[(4, ref('group_gestionnaire'))]"/>
</record>
```

### Contrôles d'Accès
```xml
<record id="access_partenariat" model="ir.model.access">
    <field name="name">Partenariat Access</field>
    <field name="model_id" ref="model_gestion_comptable_sfec_partenariat"/>
    <field name="perm_read" eval="1"/>
    <field name="perm_write" eval="1"/>
    <field name="perm_create" eval="1"/>
    <field name="perm_unlink" eval="1"/>
    <field name="group_id" ref="group_admin"/>
</record>
```

## Règles de Validation

### Contraintes Python
```python
@api.constrains('date_debut', 'date_fin')
def _check_dates(self):
    for record in self:
        if record.date_debut and record.date_fin:
            if record.date_debut > record.date_fin:
                raise ValidationError('La date de début doit être antérieure à la date de fin')
```

## Exemples d'Utilisation

### Création d'un Partenariat
```python
# Créer un nouveau partenariat
partenariat = self.env['gestion_comptable_sfec.partenariat'].create({
    'name': 'SPIRAX SARCO',
    'type_partenariat': 'spirax',
    'date_debut': '2023-01-01',
    'date_fin': '2024-12-31',
    'conditions': 'Conditions spécifiques'
})
```

## Best Practices

1. Toujours vérifier les droits d'accès avant les modifications
2. Utiliser les hooks pour la validation des données
3. Implémenter les contraintes SQL pour les règles métier
4. Utiliser les logs pour le suivi des actions
5. Documenter les changements importants
