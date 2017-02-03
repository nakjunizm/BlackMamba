import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule, JsonpModule } from '@angular/http';
import { ChartsModule } from 'ng2-charts/ng2-charts';
import { MaterialModule } from '@angular/material';
import 'hammerjs';
import { CalendarModule } from 'primeng/primeng';
import { ListboxModule } from 'primeng/primeng';
import { CheckboxModule, DataListModule, DialogModule } from 'primeng/primeng';
import { Header, Footer } from 'primeng/primeng';
import { TabViewModule } from 'primeng/primeng';

import { AppComponent } from './app.component';
import { BarChartTop10Component } from './bar.component';
import { EventListComponent } from './event-list.component';

@NgModule({
  declarations: [
    AppComponent,
    BarChartTop10Component,
    EventListComponent
  ],
  imports: [
    MaterialModule.forRoot(),
    BrowserModule,
    FormsModule,
    HttpModule,
    JsonpModule,
    ChartsModule,
    CalendarModule,
    ListboxModule,
    CheckboxModule,
    DataListModule,
    DialogModule,
    TabViewModule
  ],
  providers: [],
  bootstrap: [
    AppComponent,
    BarChartTop10Component,
    EventListComponent

  ]
})
export class AppModule { }
