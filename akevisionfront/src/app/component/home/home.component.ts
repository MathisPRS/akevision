import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { CompagnieDialogComponent } from '../compagnie-dialog/compagnie-dialog.component';
import { ClientDialogComponent } from '../client-dialog/client-dialog.component';
import { ApiService } from '../../services/api.service';
import { interval, Subscription } from 'rxjs';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {
  compagnieMessage = '';
  postes: any[] = [];
  intervalRef: any;


  constructor(private dialog: MatDialog,
    private apiService: ApiService,
    ) {}

    ngOnInit(): void {
      this.fetchPostes();
      this.intervalRef = setInterval(() => {
        this.fetchPostes();
      }, 10000);
    }
    
    ngOnDestroy(): void {
      clearInterval(this.intervalRef);
    }

  fetchPostes(): void {
    this.apiService.getAllPoste({ last_communication__isnull: false }).subscribe(postes => {
      this.postes = postes;
      console.log(postes)
      
    });
  }

  openCompagnieDialog(): void {
    const dialogCompagnieRef = this.dialog.open(CompagnieDialogComponent, {
      width: '350px',
      height :'220px'
      
    });

    dialogCompagnieRef.afterClosed().subscribe(result => {
      if (result) {
        this.compagnieMessage = "La compagnie a été créée avec succès";
      }
    });
  }

  openAgentDialog() {
    this.apiService.getAllCompagnies().subscribe(compagnies => {
      const dialogAgentRef = this.dialog.open(ClientDialogComponent, {
        width: '400px',
        data: { compagnies: compagnies }
      });
      console.log(compagnies)
      dialogAgentRef.afterClosed().subscribe(result => {
        if (result) {
          this.compagnieMessage = "La compagnie a été créée avec succès";
        }
      });
    });
  }


}
