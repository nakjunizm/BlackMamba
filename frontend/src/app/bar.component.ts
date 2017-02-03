import { Component, ViewChild, OnInit} from '@angular/core';
import { HttpService } from './http-service.component';

interface top10Obj {
    doc_count:number;
    key:string;
}

@Component({
    selector: 'top10-chart',
    templateUrl: './bar-chart-top10.html',
    providers: [ HttpService ]
})
export class BarChartTop10Component implements OnInit {

    buttonName:string = "reduction";
    chartWidth:string = "1224px";
    chartHeight:string = "612px";
    el:any;
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
        this.el = this.httpChart.nativeElement;
        this.el = this.httpsChart.nativeElement;
    }

    public barChartOptions:any = {
        scaleShowVerticalLines: false,
        responsive: true,
        animation: false
    };
    public barChartLabels:string[] = ['urlA', 'urlB', 'urlC', 'urlD',
        'urlE', 'urlF', 'urlG', 'urlH', 'urlI', 'urlJ'];
    public barChartType:string = 'bar';
    public barChartLegend:boolean = true;

    public barChartData:any[] = [
        {data: [97, 88, 86, 79, 65, 59, 56, 55, 40, 28]}
    ];

    public transform():void {
        if(this.flag) {
            this.el.style.width = "400px";
            this.el.style.height = "400px";
            this.buttonName = "extension";
            this.flag = false;
        } else {
            this.el.style.width = this.chartWidth;
            this.el.style.height = this.chartHeight;
            this.buttonName = "reduction";
            this.flag = true;
        }
    }

    public getdocs():void {
        this._httpService.getDocsRestful().subscribe(
          data => this.docs = JSON.stringify(data),
          error => console.log("ERROR HTTP GET Service"),
          () => console.log("Job Done Get !")
        );
        this._httpService.getDocsRestfulRepeat().subscribe(
            data => this.convertLabelAndData(data),
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

    private convertLabelAndData(data:any):void {
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
        this.barChartLabels = newLabel;
        this.barChartData = newData;
    }
}
