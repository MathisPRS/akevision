import { Component, OnInit } from '@angular/core';
import {AlertService} from '../../services/alert.service';
import {MailService} from '../../services/mail.service';

@Component({
  selector: 'app-download',
  templateUrl: './download.component.html',
  styleUrls: ['./download.component.scss']
})
export class DownloadComponent implements OnInit {

  fileNameChoose: string;
  dataFileToImport;
  constructor(private alertService: AlertService, private mailService: MailService) {
  }

  ngOnInit(): void {
    this.fileNameChoose = 'Import Fichier';
  }

  sendMail() {
    this.mailService.send_mail({}).subscribe(res => {
        this.alertService.success('Le mail a été envoyé');
        }, error => {
        this.alertService.error(error.error);
      });
  }
}
