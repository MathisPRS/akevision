import {Observable, of} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {environment} from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export abstract class RestService {

  protected constructor(private http: HttpClient) {
  }
  // ========== UTILS ================ //

  private getInlineGetParams(getParams: any, startInline: boolean = true): string {
    let inline = '';
    Object.entries(getParams).forEach(([key, value], i) => {
      if (value || (typeof(value) !== "boolean") && value === 0)  {
        inline += `${i === 0 && startInline ? '?' : '&'}${key}=${value}`;
      }
    });
    return inline;
  }

  // ========== HTTP VERBS =========== //

  public list<T>(endpoint: string, getParams: any = {}): Observable<any> {
    const inline: string = this.getInlineGetParams(getParams, true);
    return this.http.get<T>(`${environment.baseUrl + endpoint + inline}` );
  }

  public page<T>(endpoint: string, page: number , getParams: any = {}): Observable<any> {
    const inline: string = this.getInlineGetParams(getParams, false);
    // console.log('rest: ' + `${environment.baseUrl + endpoint}?page=${page}${inline}`);
    return this.http.get<T>(`${environment.baseUrl + endpoint}?page=${page}${inline}` );
  }

  public getFile<T>(endpoint: string, getParams: any = {}, httpOptions?: any): Observable<any> {
    return this.http.post<T>(`${environment.baseUrl + endpoint}`, getParams, httpOptions);
  }

  public retrieve<T>(endpoint: string, pk: any): Observable<any> {
    return this.http.get<T>(`${environment.baseUrl + endpoint + pk}/`);
  }

  public create<T>(endpoint: string, body: any): Observable<any> {
    return this.http.post<T>(`${environment.baseUrl + endpoint}`, body);
  }

  public delete<T>(endpoint: string, pk: any): Observable<any> {
    return this.http.delete<T>(`${environment.baseUrl + endpoint}${pk ? pk + '/' : ''}`);
  }

  public update<T>(endpoint: string, pk: any, body: any): Observable<any> {
    return this.http.put<T>(`${environment.baseUrl + endpoint + pk}/`, body);
  }

  /** permet de faire la modification sur une liste d'objet */
  public updateList<T>(endpoint: string, body: any): Observable<any> {
    return this.http.put<T>(`${environment.baseUrl + endpoint}`, body);
  }

  public partialUpdate<T>(endpoint: string, pk: any, body: any): Observable<any> {
    return this.http.patch<T>(`${environment.baseUrl + endpoint + pk}/`, body);
  }

}
