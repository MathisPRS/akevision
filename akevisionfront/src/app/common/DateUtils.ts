import * as moment from 'moment';

export class DateUtils {
  public static getFormattedDate(date: Date, format = 'YYYY-MM-DD'){
    if (date) {
      return moment(date).format(format);
    }
    return null;
  }
}
