import {Injectable} from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import './rxjs-operators';
import { ReqEvent } from './reqevent'

@Injectable()
export class HttpService {

  private headers: Headers;

  constructor(private _http: Http){}

  getDocsRestful(type:string){
    let _top10Url:string = 'http://localhost:8000/top10/'+type;
    return this._http.get(_top10Url)
                    .map(res => res.json())
                    .catch(this.handleError);
  }

  getDocsRestfulRepeat(type:string){
    console.log('in');
    let _top10Url:string = 'http://localhost:8000/top10/'+type;
    return Observable.interval(3000)
                    .switchMap(() => this._http.get(_top10Url)
                    .map(res => res.json()))
                    .catch(this.handleError);
  }

  postResAvg(fromDate:string, toDate:string) {
    let _resAvgUrl:string = 'http://localhost:8000/avg-res-time';
    let _toParam = JSON.stringify({ reference_date_from: fromDate,
                                    reference_date_to: toDate})
    return this._http.post(_resAvgUrl, _toParam)
                    .toPromise()
                    .catch(this.handleError)
  }

  getEvents(){
    let _top10Url:string = 'http://localhost:8000/avg-res-time';
    return this._http.get(_top10Url)
                    .map(res => res.json())
                    .catch(this.handleError);
  }

  updateCollector(){
    let _avgResTimeUrl:string = 'http://localhost:8000/avg-res-time/updateCollector';
    return this._http.get(_avgResTimeUrl)
                    .map(res => res.json())
                    .catch(this.handleError);
  }

  getReqEventList(): Promise<ReqEvent[]> {
    let _reqEventUrl:string = 'http://localhost:8000/event';
    return this._http.get(_reqEventUrl)
              .toPromise()
              .then(res => res.json().rst as ReqEvent[])
              .catch(this.handleError);
  }

  updateReqEventChecked(id: string, docType:string) {
    let _reqEventUrl:string = 'http://localhost:8000/event';
    let _toParam = JSON.stringify({ doc_type: docType})
    return this._http.put(_reqEventUrl + "/" + id, _toParam)
                .toPromise()
                .then(res => res.json())
                .catch(this.handleError);
  }

  private handleError (error: Response) {
    console.error(error)
    return Observable.throw(error.json() || 'error')
  }

  private _testReqEventList(){
    let events:Array<any> = new Array(5);
    for (var idx = 0; idx < 5; idx++) {
      let method:string = ''
      switch(idx % 4) {
        case 0:
          method = "GET";
          break;
        case 1:
          method = "PUT";
          break;
        case 2:
          method = "POST";
          break;
        case 3:
          method = "DELETE";
          break;
      }
      let reqEventObj = {
        type: "http",
        accesslogId: String(idx),
        requestMethod: method,
        requestUri: "/api/v1/test" + idx,
        responseCode: "200",
        responseTime: String((idx + 1) * 1000),
        isChecked: false
      }
      events[idx] = reqEventObj;
    }

    return events;
  }
}
