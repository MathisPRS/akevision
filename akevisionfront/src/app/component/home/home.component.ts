import {Component   } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ApiService  } from '../../services/api.service';
import { CompagnieService } from '../../services/compagnie.service';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})

export class HomeComponent {
  compagnie = {
    name: ''
  };
  compagnieMessage = '';
  
  constructor(private compagnieService: CompagnieService) { }

  onSubmit() {
    this.compagnieService.createCompagnie(this.compagnie).subscribe(
      response => {
        this.compagnieMessage = "La compagnie a été créé"
    },
      error => {
        if (error.error && error.error.name) {
          this.compagnieMessage = error.error.name[0];
          
        } else {
          this.compagnieMessage = 'Une erreur s\'est produite. Veuillez réessayer.';
        }
      }
    );
  }
}