import { Component, ViewChild, OnInit} from '@angular/core';

// webpack html imports
let template = require('./bar-chart-top10.html');

@Component({
    selector: 'top10-chart',
    template: template
})
export class BarChartTop10Component implements OnInit {

    buttonName:string = "reduction";
    chartWidth:string = "1224px";
    chartHeight:string = "612px";
    el:any;
    flag:boolean = true;

    @ViewChild("myChart") myChart;

    ngOnInit() {
        this.el = this.myChart.nativeElement;
    }

    public barChartOptions:any = {
        scaleShowVerticalLines: false,
        responsive: true
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
}