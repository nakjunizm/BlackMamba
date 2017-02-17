import { Component, OnInit } from '@angular/core';
import { HttpService } from './http-service.component';
import { ReqEvent } from './reqevent';

@Component({
  selector: 'event-list',
  templateUrl: './event-list.component.html',
  providers: [ HttpService ]
})
export class EventListComponent implements OnInit {

  reqEvents: ReqEvent[];
  selectedReqEvent: ReqEvent;
  displayDialog: boolean;
  docs:string;
  get_events_buttonName:string='Get Event List'

  constructor(private _httpService:HttpService){}

  ngOnInit() {
    this._httpService.getReqEventList().then(reqEvents => this.reqEvents = reqEvents);
  }

  public get_events():void {
    this._httpService.getEvents().subscribe(
        data => this.docs = JSON.stringify(data),
        error => console.log("ERROR HTTP GET Service"),
        () => console.log("Job Done Get repeat!")
    );
  }

  reqEventClick(reqEvent:ReqEvent):void {
    //TODO: dataList Refresh
    this._httpService.updateReqEventChecked(reqEvent.id, reqEvent.type)
                      .then(res => this.callbackRefresh(res));
  }

  selectReqEvent(reqEvent: ReqEvent) {
    this.selectedReqEvent = reqEvent;
    this.displayDialog = true;
  }

  onDialogHide() {
    this.selectedReqEvent = null;
  }

  callbackRefresh(data:any):any {
    console.log(data)
    this._httpService.getReqEventList().then(reqEvents => this.reqEvents = reqEvents);
  }
}
