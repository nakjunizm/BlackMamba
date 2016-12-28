import { Component, OnInit } from '@angular/core';
import { HttpService } from './http-service.component';
import { SelectItem } from 'primeng/primeng';

@Component({
  selector: 'event-list',
  templateUrl: './event-list.component.html',
  providers: [ HttpService ]
})
export class EventListComponent implements OnInit {

  constructor(private _httpService:HttpService){
    this.events = [];
    this.events.push({label:'urlA', value:'urlA'});
    this.events.push({label:'urlB', value:'urlB'});
    this.events.push({label:'urlC', value:'urlC'});
    this.events.push({label:'urlD', value:'urlD'});
    this.events.push({label:'urlE', value:'urlE'});
    this.events.push({label:'urlF', value:'urlF'});
  }
  docs:string;
  get_events_buttonName:string='Get Event List'
  private myDatePickerOptions = {
    todayBtnTxt: 'Today',
    dateFormat: 'yyyy-mm-dd',
    firstDayOfWeek: 'mo',
    sunHighlight: true,
    height: '34px',
    width: '260px',
    inline: false,
    selectionTxtFontSize: '16px'
  };
  private selectedDate:string = '';
  private selectedText: string = '';
  private border: string = 'none';
  date111:Date;
  selectedEvent: string[];

  ngOnInit() {
        console.log('onInit(): DatePicker OnInit');
  }

  // onDateChanged(event:any) {
  //     console.log('onDateChanged(): ', event.date, ' - jsdate: ', new Date(event.jsdate).toLocaleDateString(), ' - formatted: ', event.formatted, ' - epoc timestamp: ', event.epoc);
  //     if(event.formatted !== '') {
  //         this.selectedText = 'Formatted: ' + event.formatted + ' - epoc timestamp: ' + event.epoc;
  //         this.border = '1px solid #CCC';
  //
  //         this.selectedDate = event.formatted;
  //     }
  //     else {
  //         this.selectedText = '';
  //         this.border = 'none';
  //     }
  // }
  //
  // onInputFieldChanged(event:any) {
  //   console.log('onInputFieldChanged(): Value: ', event.value, ' - dateFormat: ', event.dateFormat, ' - valid: ', event.valid);
  // }
  //
  // onCalendarViewChanged(event:any) {
  //   console.log('onCalendarViewChanged(): Year: ', event.year, ' - month: ', event.month, ' - first: ', event.first, ' - last: ', event.last);
  // }

  events:SelectItem[];
  selectedItime:string;

  public get_events():void {
    this._httpService.getEvents().subscribe(
        data => this.docs = JSON.stringify(data),
        error => console.log("ERROR HTTP GET Service"),
        () => console.log("Job Done Get repeat!")
    );
  }
}
