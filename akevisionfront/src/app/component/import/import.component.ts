import { Component, OnInit } from '@angular/core';
import {AlertService} from '../../services/alert.service';
import {UploadFileService} from '../../services/upload-file.service';

@Component({
  selector: 'app-import',
  templateUrl: './import.component.html',
  styleUrls: ['./import.component.scss']
})
export class ImportComponent implements OnInit {

  fileNameChoose: string;
  dataFileToImport;
  constructor(private alertService: AlertService, private uploadFileService: UploadFileService) {
  }

  ngOnInit(): void {
    this.fileNameChoose = 'Import Fichier';
  }

  onSubmit(event){
    this.saveOperation();
  }



  calculateIfImportFile() {
    return !!this.dataFileToImport;
  }

  exelInputChange(event) {
    this.dataFileToImport = event;
    if (event.target.files[0] && event.target.files[0]) {
      this.fileNameChoose = event.target.files[0].name;
    }
  }

  saveOperation(){
      if (this.dataFileToImport) {
        this.launchLoadImportFile();
    } else {
      this.alertService.error('Il faut au moin un type pour importer le fichier');
    }
  }

  launchLoadImportFile() {
    this.uploadFileService.postFile(this.dataFileToImport.target.files[0]).subscribe(res => {
        this.alertService.success('Le fichier a été importé');
        }, error => {
        this.alertService.error(error.error);
      });
  }



}
