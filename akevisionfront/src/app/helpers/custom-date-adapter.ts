import {NativeDateAdapter} from '@angular/material/core';
import {Injectable} from '@angular/core';

@Injectable()
export class CustomDateAdapter extends NativeDateAdapter {

  override parse(value: any): Date | null {
        if ((typeof value === 'string') && (value.indexOf('/') > -1) && (value.indexOf(':') === -1)) {
          const str = value.split('/');
          const year = Number(str[2]);
          const month = Number(str[1]) - 1;
          const date = Number(str[0]);
          return new Date(year, month, date);
        }
        if ((typeof value === 'string') && (value.indexOf('/') > -1) && (value.indexOf(':') > -1)
          && (value.indexOf(' ') > -1)) {
          const dateListTime = value.split(' '); // sépare la date du time
          const dateList = dateListTime[0].split('/');
          const year = Number(dateList[2]);
          const month = Number(dateList[1]) - 1;
          const date = Number(dateList[0]);
          const timeList = dateListTime[1].split(':');
          const hour = Number(timeList[0]);
          const min = Number(timeList[1]);
          return new Date(year, month, date, hour, min);
        }
        const timestamp = typeof value === 'number' ? value : Date.parse(value);
        return isNaN(timestamp) ? null : new Date(timestamp);
      }

  override format(date: Date, displayFormat: string): string {
       if (displayFormat === 'input') {
          // affiche l'input sous le format dd/MM/yyyy
          const day = date.getDate();
          const month = date.getMonth() + 1;
          const year = date.getFullYear();
          return this._to2digit(day) + '/' + this._to2digit(month) + '/' + year;

       } else if (displayFormat === 'inputMonth') {
          // affiche monthYearLabel en francais
          return date.toLocaleDateString('fr-FR',  { month: 'short', year: 'numeric' });
       } else if (displayFormat === 'inputtime') {
          // affiche l'input sous le format dd/MM/yyyy hh:mm
          const day = date.getDate();
          const month = date.getMonth() + 1;
          const year = date.getFullYear();
          const hour = date.getHours();
          const min = date.getMinutes();
          return this._to2digit(day) + '/' + this._to2digit(month) + '/' + year + ' ' + hour + ':' + min;

       } else if (displayFormat === 'popupHeaderDate') {
          // affiche nom du jour, mois, numéro du jour en francais
          return date.toLocaleDateString('fr-FR',  { weekday: 'short', month: 'short', day: '2-digit' });
       } else {
           return date.toDateString();
       }
   }

   private _to2digit(n: number) {
       return ('00' + n).slice(-2);
   }
}

export const APP_DATE_FORMATS =
{
  parse: {
    dateInput: {month: 'short', year: 'numeric', day: 'numeric'},
    datetimeInput: {month: 'short', year: 'numeric', day: 'numeric'},
    },
  display: {
    dateInput: 'input',
    monthYearLabel: 'inputMonth',
    dateA11yLabel: {year: 'numeric', month: 'long', day: 'numeric'},
    monthYearA11yLabel: {year: 'numeric', month: 'long'},
    datetimeInput: 'inputtime',
    popupHeaderDateLabel: 'popupHeaderDate',
  }
};
