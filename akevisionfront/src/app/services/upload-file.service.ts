import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';
import {RestService} from './rest.service';
import {HttpClient, HttpEvent, HttpErrorResponse, HttpEventType} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UploadFileService {
  static URL_BASE = '/manage-file/';
  static URL_upload_file = '/manage-file/upload_select_file/';

  constructor(private http: RestService, private httpClient: HttpClient) { }

  public postFile(fileToUpload: File): Observable<any> {
    const formData: FormData = new FormData();
    formData.append('fileKey', fileToUpload, fileToUpload.name);
    return this.http.create(UploadFileService.URL_upload_file, formData);
  }
}

