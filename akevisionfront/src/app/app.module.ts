import { BrowserModule } from '@angular/platform-browser';
import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { LoginComponent } from './component/login/login.component';
import { RegisterComponent } from './component/register/register.component';
import { AlertComponent } from './component/alert/alert.component';
import {ErrorInterceptor} from './helpers/error.interceptor';
import {TokenInterceptor} from './helpers/token.interpector';
import { AppComponent } from './app.component';
import { HomeComponent } from './component/home/home.component';
import { SortableDirective } from './directives/sortable.directive';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MaterialModule} from './material-module';
import { TestMatMaterialComponent } from './component/test-mat-material/test-mat-material.component';
import { MatDatetimepickerModule, MatNativeDatetimeModule } from '@mat-datetimepicker/core';
import { registerLocaleData } from '@angular/common';
import localeFr from '@angular/common/locales/fr';
import {DateAdapter, MAT_DATE_FORMATS} from '@angular/material/core';
import {APP_DATE_FORMATS, CustomDateAdapter}  from './helpers/custom-date-adapter';
import {MAT_DATETIME_FORMATS} from '@mat-datetimepicker/core';
import { ImportComponent } from './component/import/import.component';
import { DownloadComponent } from './component/download/download.component';
registerLocaleData(localeFr, 'fr');

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    RegisterComponent,
    AlertComponent,
    SortableDirective,
    TestMatMaterialComponent,
    ImportComponent,
    DownloadComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    MaterialModule,
    MatNativeDatetimeModule,
    MatDatetimepickerModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: TokenInterceptor, multi: true },
    { provide: DateAdapter, useClass: CustomDateAdapter },
    { provide: MAT_DATE_FORMATS, useValue: APP_DATE_FORMATS },
    { provide: MAT_DATETIME_FORMATS, useValue: APP_DATE_FORMATS },
  ],
  bootstrap: [AppComponent , LoginComponent ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule { }
