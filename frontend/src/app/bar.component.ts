import { Component, ViewChild, OnInit} from '@angular/core';
import { HttpService } from './http-service.component';

@Component({
    selector: 'top10-chart',
    templateUrl: './bar.component.html',
    providers: [ HttpService ]
})
export class BarChartTop10Component implements OnInit {

    buttonName:string = "reduction";
    chartWidth:string = "1224px";
    chartHeight:string = "612px";
    http_el:any;
    https_el:any;
    flag:boolean = true;

    getdocs_buttonName:string = 'getDocs';

    postAvgBtn:string = 'Response_AVG';
    updateCollectorBtn:string = 'updateCollector';
    docs:string;
    data:any;

    constructor(private _httpService:HttpService){}

    @ViewChild("httpChart") httpChart;
    @ViewChild("httpsChart") httpsChart;

    ngOnInit() {
        this.http_el = this.httpChart.nativeElement;
        this.https_el = this.httpsChart.nativeElement;
    }

    public barChartOptions:any = {
        scaleShowVerticalLines: false,
        responsive: true,
        animation: false
    };
    public httpLabels:string[] = ['urlA', 'urlB', 'urlC', 'urlD',
        'urlE', 'urlF', 'urlG', 'urlH', 'urlI', 'urlJ'];
    public httpsLabels:string[] = ['AAA', 'BBB', 'CCC', 'DDD',
        'EEE', 'FFF', 'GGG', 'HHH', 'III', 'JJJ'];
    public barChartType:string = 'bar';
    public barChartLegend:boolean = true;

    public httpData:any[] = [
        {data: [97, 88, 86, 79, 65, 59, 56, 55, 40, 28]}
    ];
    public httpsData:any[] = [
        {data: [60, 50, 60, 27, 80, 100, 60, 90, 30, 40]}
    ];

    public transform():void {
        if(this.flag) {
            this.http_el.style.width = "400px";
            this.http_el.style.height = "400px";
            this.buttonName = "extension";
            this.flag = false;
        } else {
            this.http_el.style.width = this.chartWidth;
            this.http_el.style.height = this.chartHeight;
            this.buttonName = "reduction";
            this.flag = true;
        }
    }

    public getdocs():void {
        this._httpService.getDocsRestful('http').subscribe(
          data => this.docs = JSON.stringify(data),
          error => console.log("ERROR HTTP GET Service"),
          () => console.log("Job Done Get !")
        );
        this._httpService.getDocsRestfulRepeat('http').subscribe(
            data => this.convertLabelAndData('http',data),
            error => console.log("ERROR HTTP GET Service"),
            //() => this.convertLabelAndData()
            () => console.log("Job Done Get repeat!")
        );
        this._httpService.getDocsRestfulRepeat('https').subscribe(
            data => this.convertLabelAndData('https',data),
            error => console.log("ERROR HTTP GET Service"),
            //() => this.convertLabelAndData()
            () => console.log("Job Done Get repeat!")
        );

    }

    public postAvg():void {
        let _fromDate:string = "2016-12-01";
        let _toDate:string = "2016-12-11";
        this._httpService.postResAvg(_fromDate, _toDate).subscribe(
            () => console.log("postAvg Job Done")
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
        console.log(data)
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
