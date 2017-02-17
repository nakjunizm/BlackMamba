import { Component } from '@angular/core';
import { HttpService } from './http-service.component';

@Component({
  selector: 'calc',
  templateUrl: './calc.component.html',
  providers: [ HttpService ]
})
export class CalcComponent {

  postAvgBtn:string = 'Response_AVG';
  dateFrom:Date;
  dateTo:Date;

  constructor(private _httpService:HttpService){}

  public postAvg():void {
    if(this.dateFrom == null || this.dateTo == null) {
      alert("Please Check the date");
      return;
    }
    let _fromDate:string = this.dateFrom.toLocaleDateString().replace(/\./g,"").replace(/ /g, "-",);
    let _toDate:string = this.dateTo.toLocaleDateString().replace(/\./g,"").replace(/ /g, "-");
    this._httpService.postResAvg(_fromDate, _toDate).then();
  }
}