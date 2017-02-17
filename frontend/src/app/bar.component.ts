import { Component, ViewChild, OnInit} from '@angular/core';
import { HttpService } from './http-service.component';

@Component({
    selector: 'top10-chart',
    templateUrl: './bar.component.html',
    providers: [ HttpService ]
})
export class BarChartTop10Component implements OnInit {

  bar_tab_names:string[] = ["http", "https"]
  http_el:any;
  https_el:any;
  flag:boolean = true;

  getdocs_buttonName:string = 'getDocs';

  postAvgBtn:string = 'Response_AVG';
  updateCollectorBtn:string = 'updateCollector';
  docs:string;
  data:any;

  constructor(private _httpService:HttpService){}

  ngOnInit() {
    this.bar_tab_names.map(
    name => this._httpService.getDocsRestful(name)
            .then(data => this.convertLabelAndData(name, data))
    );
  }

  public barChartOptions:any = {
      scaleShowVerticalLines: false,
      responsive: true,
      animation: false
  };
  public httpLabels:string[] = null;
  public httpsLabels:string[] = null;
  public barChartType:string = 'bar';
  public barChartLegend:boolean = false;

  public httpData:any[] = [
    {data: [97, 88, 86, 79, 65, 59, 56, 55, 40, 28]}
  ];
  public httpsData:any[] = [
    {data: [60, 50, 60, 27, 80, 100, 60, 90, 30, 40]}
  ];

  public getdocs():void {
    this._httpService.getDocsRestfulRepeat('http').subscribe(
      data => this.convertLabelAndData('http',data),
      error => console.log("ERROR HTTP GET Service"),
      () => console.log("Job Done Get repeat!")
    );
    this._httpService.getDocsRestfulRepeat('https').subscribe(
      data => this.convertLabelAndData('https',data),
      error => console.log("ERROR HTTP GET Service"),
      () => console.log("Job Done Get repeat!")
    );

  }

  public updateCollector():void {
    this._httpService.updateCollector().subscribe(
        data => this.docs = JSON.stringify(data),
        error => console.log("ERROR HTTP GET Service"),
        () => console.log("Job Done Get !")
    );
  }

  private convertLabelAndData(type:string, data:any):void {
    let newLabel:Array<string> = new Array(10);
    let newData:Array<any> = new Array(1);
    newData[0] = {data: new Array(10)};
    let buckets:any[] = data.aggregations.avg_response_time.buckets;
    let i = 0
    buckets.forEach(function(item){
        newLabel[i] = item.key;
        newData[0].data[i] = item.doc_count;
        i++;
    });
    if(type == 'http') {
        this.httpLabels = newLabel;
        this.httpData = newData;
    } else {
        this.httpsLabels = newLabel;
        this.httpsData = newData;
    }
  }
}
