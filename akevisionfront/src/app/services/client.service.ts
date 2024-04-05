import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { saveAs } from 'file-saver';

@Injectable({
  providedIn: 'root'
})
export class ClientService {

  constructor(private http: HttpClient, private apiService: ApiService) { }

  createClient(client: any): Observable<any> {
    return this.apiService.post('/clients/', {
      name: client.name,
      os: client.os,
      compagnie_id: client.compagnie_id,
      ipv4: client.ipv4
    });
  }

  getScriptClient(id_client : number ): Observable<any> { 
    
    return this.apiService.get('/clients/'+id_client+'/download-script',{ responseType: 'blob' });

    }

 downloadFile(data: Blob, filename: string): void {
    saveAs(data, filename);
  }
}
