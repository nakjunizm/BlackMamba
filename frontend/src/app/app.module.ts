import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule, JsonpModule } from '@angular/http';
import { ChartsModule } from 'ng2-charts/ng2-charts';
import { MaterialModule } from '@angular/material';
import 'hammerjs';
import { CalendarModule } from 'primeng/primeng';
import { ListboxModule } from 'primeng/primeng';
import { ChartModule } from 'primeng/primeng';
import { TabViewModule } from 'primeng/primeng';

import { AppComponent } from './app.component';
import { BarChartTop10Component } from './bar.component';
import { EventListComponent } from './event-list.component';
import { ChartComponent } from './chart.component'

@NgModule({
  declarations: [
    AppComponent,
    BarChartTop10Component,
    EventListComponent,
    ChartComponent
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
    ChartModule,
    TabViewModule
  ],
  providers: [],
  bootstrap: [
    AppComponent,
    BarChartTop10Component,
    EventListComponent,
    ChartComponent

  ]
})
export class AppModule { }
