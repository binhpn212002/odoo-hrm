/** @odoo-module */

export class OdooConvert {
    static convertToOdooDateFormat(dateStr) {
        const [month, day, year] = dateStr.split('/');
        const dateObject = new Date(`${year}-${month}-${day}`);
        return dateObject.toISOString().split('T')[0];
    }
}
