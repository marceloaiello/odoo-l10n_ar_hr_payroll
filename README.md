# Odoo Payroll - Localizacion Argentina
Odoo Payroll and HR Addons - l10n_ar: Localización Argentina

La localizacion argentina de payroll para odoo, permite liquidar sueldos de acuerdo a las leyes y regulaciones Argentinas, asi como liquidar las cargas sociales correctamente con los sistemas de AFIP. Provee soporte para sindicatos, integracion con sistemas AFIP, y demas funciones que extienden y mejoran la implementacion actual de payroll de odoo.

## Descripcion de los Modulos

* "hr_labor_union" - Soporte para sindicatos en Argentina. Agrega la posibilidad de parametrizar sindicatos, sus escalas, precios, actualizaciones y seguros sindicales,
para ser usados en la liquidacion de sueldos.
* "hr_overtime" - Soporte para ingreso manual o automatico (desde hr_attendance) de horas extra y su discriminacion en recibos de sueldo segun su categoria (50% - 100%).
* "l10n_ar_afip_sicoss" - Agrega los campos registrales requeridos en los sistemas de AFIP y automatiza la generacion de .txt para liquidaciones de cargas sociales 931, libro sueldos, sicoss.
* "l10n_ar_hr_ux" - Agrega varios cambios esteticos y funcionales a las vistas de hr y payroll para adaptarlo al funcionamiento en Argentina.
* "l10n_ar_payroll" - Agrega funciones y tablas al modulo de Payroll para la liquidacion de sueldos en Argentina.
* "l10n_ar_payroll_lu_*****" - Implementaciones de tablas y funcionalidades de distintos sindicatos de Argentina. Actualmente soportados: UOM, ASIMRA.

## Roadmap and TODOs

A continuacion, listamos los siguientes cambios y nuevas funciones que se encuentran en desarrollo o que estan pendientes para desarrollar en el modulo. Si ud. desea colaborar
con el proyecto, aceptamos pull requests y le sugerimos comenzar con las tareas pendientes de la siguiente lista. Si

* (Prioridad: MEDIA) - Realizar vinculacion entre el modulo hr_fleet para poder seleccionar en empleados, los vehiculos vinculados a ese empleado. Ademas de la relacion con el
vehiculo, se debera proveer una forma rapida de ver datos como patente, etc.
* (Prioridad: BAJA) - Soporte para distintas tarjetas de mobilidad (SUBE, etc). Actualmente el sistema permite ingresar una sola tarjeta de mobilidad.
* (Prioridad: MEDIA) - Implementacion y soporte para el calculo automatico de dias de vacaciones y asignacion automatica de los dias en el modulo hr_leave.
* (Prioridad: MEDIA) - Automatizacion de payslip batches para que los mismos sean "pre-liquidados" en las fechas configuradas.
* (Prioridad: MEDIA) - Soporte de estadisticas de payroll.
* (Prioridad: BAJA) - Report separado para registros de contribucion. Puede ser util para contadores y prestancion de DDJJ.
* (Prioridad: ALTA) - Implementacion de creacion de txt de SICOSS. Importacion automatica a 931.
* (Prioridad: ALTA) - Implementacion (en las distintas sub-localizaciones de sindicatos) de los disños de registro de importacion de informacion a sistemas sindicales. Se debe crear primero un modulo generico, que permita la facil implementacion de distintos diseños en cada sub-localizacion sindical. Se
* (Prioridad: ALTA) - Calculo automatico de estados de AFIP (en hr_contract) basado en acciones con botones que permitan agilizar la carga de empleados en ILT, cambio automatico de estado de periodos de prueba y estados de revista. (mas info en el archivo hr_contract.py),
* (Prioridad: ALTA) - Posibilidad de añadir periodos predefinidos en la creacion del recibo de sueldo.
* (Prioridad: ALTA) - Implementar modelo de adelantos y prestamos a los empleados, el cual luego debe popular los inputs de ADV-AMOUNT y LOAN-AMOUNT.
