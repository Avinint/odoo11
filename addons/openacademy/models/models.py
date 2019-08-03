# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import timedelta
import math

class Course(models.Model):
    _name = 'openacademy.course'
    _description = "OpenAcademy Courses"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one( 'res.users', on_delete='set null', string="Responsible", index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions", copy=False)
    _sql_constraints = [('name_description_check',
                         'CHECK(name != description)',
                         'The title of the course should not be the description'),
                        ('name_unique', 'UNIQUE(name)', 'Course title should be unique')]


    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        #testing orm methods
        for user in self.env['res.users'].browse(1,2,7):
            print(user.name)

        def get_original_course_name(src_name):
            if "Copy of" in src_name:
                new_name = src_name.replace("Copy of ", "")
                if any([b in new_name for b in ("(", ")")]):
                    return new_name[:new_name.index('(') -1]
                return new_name
            return src_name

        def edit_existing_name():
            copied_count = self.search_count([('name', '=like', u"Copy of {}%".format(name))])
            if not copied_count:
                return f"Copy of {name}"
            return f"Copy of {name} ({copied_count})"

        name = get_original_course_name(self.name)
        default['name'] = edit_existing_name()
        return super(Course, self).copy(default)


    # @api.multi
    # def copy(self, default=None):
    #     default= dict(default or {})
    #     copied_count = self.search_count(
    #         [('name', '=like', f"Copy of {self.name}")])
    #     if not copied_count:
    #         new_name = f"Copy of {self.name}"
    #     else:
    #         new_name = f"Copy of {self.name} {copied_count}"
    #
    #     default['name'] = new_name
    #     return super(Course, self).copy(default)

class Session(models.Model):
    _name = 'openacademy.session'
    _description = "Openacademy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    end_date = fields.Date(compute="_get_end_date", inverse="_set_end_date", store=True, string="End Date")
    duration = fields.Float(digits=(6,2), help="Duration in days", default=1.0)
    seats = fields.Integer(string="Number of Seats")
    taken_seats = fields.Float(compute='_taken_seats')

    instructor_id = fields.Many2one('res.partner', on_delete='set null', string="Instructor", index=True,
                                    domain=['|',('instructor','=',True),
                                                ('category_id.name','ilike','Teacher')])
    course_id = fields.Many2one('openacademy.course', on_delete='cascade',
                                string="Course", index=True, required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    active = fields.Boolean(default=True)

    @api.depends('attendee_ids', 'seats')
    def _taken_seats(self):
        for record in self:
            if not record.seats:
                record.taken_seats = 0.0
            else:
                record.taken_seats = len(record.attendee_ids) / record.seats * 100

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            r.duration = (r.end_date - r.start_date).days + 1

    @api.onchange('attendee_ids', 'seats')
    def _check_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': 'Incorrect number of seats',
                    'message': 'Negative number of seats'
                }
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': 'Too many attendees',
                    'message': 'Increase seats or Remove attendees'
                }
            }

    @api.constrains('attendee_ids', 'instructor_id')
    def check_instructor_not_attendee(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor cannot be an attendee")




