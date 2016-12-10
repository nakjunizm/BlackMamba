import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule, JsonpModule } from '@angular/http';
import { ChartsModule } from 'ng2-charts/ng2-charts';
import { MaterialModule } from '@angular/material';
import 'hammerjs';

import { AppComponent } from './app.component';
import { BarChartTop10Component } from './bar.component';

@NgModule({
  declarations: [
    AppComponent,
    BarChartTop10Component
  ],
  imports: [
    MaterialModule.forRoot(),
    BrowserModule,
    FormsModule,
    HttpModule,
    JsonpModule,
    ChartsModule
  ],
  providers: [],
  bootstrap: [AppComponent, BarChartTop10Component]
})
export class AppModule { }
