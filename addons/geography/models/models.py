# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Country(models.Model):
    _name = 'geography.country'
    _description = "All countries of the world with data"

    name = fields.Char(string="Country", required=True)
    area_id = fields.Many2one('geography.area', string="Area")
    iso = fields.Char(string="Iso")
    code = fields.Char(string="Code M49",  required=True)
    category_ids = fields.Many2many('geography.country.category', string="Categories")
    population = fields.Integer(string="Population")
    pop_male = fields.Integer(string="Population Male")
    pop_female = fields.Integer(string="Population Female")
    continent_id = fields.Many2one('geography.area', compute='_get_continent', store=True)

    _sql_constraints = [('code_unique', 'UNIQUE(code)', u'Country M49 code doit etre unique'),
                        ('iso_unique', 'UNIQUE(iso)', u'Country iso code doit etre unique'),
                        ('name_unique', 'UNIQUE(name)', u'Country name doit etre unique')]

    @api.depends('area_id')
    def _get_continent(self):
        continents = ['Europe', 'Americas', 'Africa', 'Asia', 'Oceania']
        for record in self:
            continent = record.area_id

            while continent.name not in continents:
                if continent.parent_id is None:
                    break
                continent = continent.parent_id
            record.continent_id = continent


class Area(models.Model):
    _name = 'geography.area'
    _description = "All areas of the world"

    name = fields.Char(string="Area", required=True)
    code = fields.Char(string="Code M49", required=True)
    parent_id = fields.Many2one('geography.area', string="Parent Area")
    child_ids = fields.One2many('geography.area', 'parent_id', string='Dependent Areas')
    country_ids = fields.One2many('geography.country', 'area_id', string='Countries')

    @api.onchange('name')
    def _onchange_name(self):
        world = self.search([('name', 'ilike', "World")])
        if self.name in ['Europe', 'Americas', 'Africa', 'Asia', 'Oceania']:
            self.parent_id = world

        return {}

class Category(models.Model):
    _name = 'geography.country.category'
    _description = "Development level of country"

    name = fields.Char(string="Area", required=True)
    code = fields.Char(string="Code", required=True)
    category_ids = fields.Many2many('geography.country', string="Countries")