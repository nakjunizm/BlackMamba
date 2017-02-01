import { Component, ViewChild, OnInit} from '@angular/core';
import { HttpService } from './http-service.component';
import { UIChart } from 'primeng/primeng';

@Component({
    selector: 'chart',
    templateUrl: './chart.component.html',
    providers: [ HttpService ]
})

export class ChartComponent implements OnInit {

    @ViewChild("chart") chart: UIChart;

    getdocs_buttonName: string = 'getDocs';
    docs: any;
    data: any;
    options: any;

    constructor(private _httpService:HttpService){
        this.data = {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            datasets: [
                {
                    label: 'My First dataset',
                    backgroundColor: '#42A5F5',
                    borderColor: '#1E88E5',
                    data: [65, 59, 80, 81, 56, 55, 40]
                }
            ]
        }

        this.options = {
            title: {
                display: true,
                text: 'Top10 Called uri',
                fontSize: 16
            },
            legend: {
                position: 'bottom'
            }
        };
    }

    ngOnInit() {
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
            () => console.log("Job Done Get ! repeat")
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
        this.data.labels = newLabel;
        this.data.datasets[0].data = newData;
        console.log('data : ', this.data.datasets[0].data)
        console.log('label : ', this.data.labels)

    }
}
