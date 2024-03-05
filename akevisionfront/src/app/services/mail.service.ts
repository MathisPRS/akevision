import {Injectable} from '@angular/core';
import {RestService} from './rest.service';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MailService {

  constructor(private http: RestService) { }

  static URL_BASE = '/mail/';
  static URL_SEND_MAIL = MailService.URL_BASE + 'send_mail/';

  public send_mail(filter): Observable<any> {
    return this.http.create(MailService.URL_SEND_MAIL, filter);
  }
}
