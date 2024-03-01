import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {HomeComponent} from './component/home/home.component';
import {LoginComponent} from './component/login/login.component';
import {RegisterComponent} from './component/register/register.component';
import {AuthGuard} from './helpers/auth.guard';
import {TestMatMaterialComponent} from './component/test-mat-material/test-mat-material.component';
import {DownloadComponent} from "./component/download/download.component";
import {ImportComponent} from "./component/import/import.component";

export const routes: Routes = [
  { path: '', component: HomeComponent, canActivate: [AuthGuard] },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'mat-material', component: TestMatMaterialComponent },
  { path: 'download', component: DownloadComponent },
  { path: 'import', component: ImportComponent },
  { path: 'home', component: HomeComponent },

  // otherwise redirect to home
  { path: '**', redirectTo: 'home' },
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
