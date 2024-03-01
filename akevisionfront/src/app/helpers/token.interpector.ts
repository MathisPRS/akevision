import {Injectable} from '@angular/core';
import {HttpRequest, HttpHandler, HttpEvent, HttpInterceptor} from '@angular/common/http';
import {Observable} from 'rxjs';
import {AuthentificationService} from '../services/authentification.service';
import {UserAuth} from "../model/userAuth";


@Injectable()
export class TokenInterceptor implements HttpInterceptor {
  constructor(private authentificationService: AuthentificationService) {
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // add authorization header with jwt token if available
    const currentUser: UserAuth = this.authentificationService.currentUserValue;
    if (currentUser && currentUser.token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Token ${currentUser.token}`
        }
      });
      if (currentUser.isDeleting()) {
        this.authentificationService.removeCurrentUser();
      }
    }
    return next.handle(request);
  }
}
