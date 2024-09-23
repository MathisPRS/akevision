import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { CompagnieDialogComponent } from '../compagnie-dialog/compagnie-dialog.component';
import { ClientDialogComponent } from '../client-dialog/client-dialog.component';
import { ApiService } from '../../services/api.service';
import { interval, Subscription, forkJoin } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {
  compagnieMessage = '';
  postes: any[] = [];
  compagnies: any[] = [];
  intervalRef: any;

  constructor(private dialog: MatDialog, private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchData();
    this.intervalRef = setInterval(() => {
      this.fetchPostes();
    }, 5000);
  }

  ngOnDestroy(): void {
    clearInterval(this.intervalRef);
  }

  fetchData(): void {
    forkJoin({
      compagnies: this.apiService.getAllCompagnies(),
      postes: this.apiService.getAllPoste({ last_communication__isnull: false })
    }).subscribe(({ compagnies, postes }) => {
      this.compagnies = compagnies.map(compagnie => ({ ...compagnie, isExpanded: false }));
      this.postes = postes;
      console.log('Compagnies:', this.compagnies);
      console.log('Postes:', this.postes);
      this.sortPostesByCompagnie();
    });
  }

  fetchPostes(): void {
    this.apiService.getAllPoste({ last_communication__isnull: false }).subscribe(postes => {
      this.postes = postes;
      this.sortPostesByCompagnie();
    });
  }

  sortPostesByCompagnie(): void {
    this.compagnies.forEach(compagnie => {
      compagnie.postes = this.postes.filter(poste => poste.compagnie_id === compagnie.id);
    });
  }

  toggleExpand(compagnie: any): void {
    compagnie.isExpanded = !compagnie.isExpanded;
  }

  openCompagnieDialog(): void {
    const dialogCompagnieRef = this.dialog.open(CompagnieDialogComponent, {
      width: '350px',
      height: '220px'
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
      dialogAgentRef.afterClosed().subscribe(result => {
        if (result) {
          this.compagnieMessage = "La compagnie a été créée avec succès";
        }
      });
    });
  }
}
