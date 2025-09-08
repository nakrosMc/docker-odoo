from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import UserError

@tagged('post_install', '-at_install', 'leave_motive')
class TestHrLeaveMotive(TransactionCase):
    """
    Pruebas para validar la creación y asignación de motivos de ausencia.
    """

    def setUp(self):
        super(TestHrLeaveMotive, self).setUp()
        # Crear un usuario de prueba para las operaciones
        self.user_employee = self.env['res.users'].create({
            'name': 'Empleado de Prueba',
            'login': 'test_employee',
            'email': 'test@example.com',
        })
        # Crear un empleado asociado al usuario
        self.employee = self.env['hr.employee'].create({
            'name': 'Empleado de Prueba',
            'user_id': self.user_employee.id
        })
        # Crear un tipo de ausencia
        self.leave_type = self.env['hr.leave.type'].create({
            'name': 'Días Libres de Prueba',
            'requires_allocation': 'no',
        })
        # Crear un motivo de ausencia
        self.motive = self.env['hr.leave.motive'].create({'name': 'Cita Médica'})

    def test_01_create_and_assign_motive(self):
        """
        Prueba la creación de una ausencia con un motivo y verifica que se guarde correctamente.
        """
        # Crear una ausencia como el empleado de prueba
        leave = self.env['hr.leave'].with_user(self.user_employee).create({
            'name': 'Ausencia por prueba',
            'employee_id': self.employee.id,
            'holiday_status_id': self.leave_type.id,
            'request_date_from': '2025-10-10',
            'request_date_to': '2025-10-10',
            'motive_id': self.motive.id,  # Asignar el motivo creado
        })

        # Verificar que la ausencia se creó
        self.assertTrue(leave.exists(), "La ausencia no se pudo crear.")
        
        # Verificar que el motivo se asignó correctamente
        self.assertEqual(leave.motive_id, self.motive, "El motivo de la ausencia no coincide.")
        self.assertEqual(leave.motive_id.name, 'Cita Médica', "El nombre del motivo no es el esperado.")

        # Imprimir un mensaje de éxito para la consola de pruebas
        print("Prueba 'test_01_create_and_assign_motive' finalizada con éxito.")