import {Injectable} from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import './rxjs-operators';

@Injectable()
export class HttpService {

  private headers: Headers;

  constructor(private _http: Http){
    this.headers = new Headers();
    // this.headers.append('Content-Type', 'application/json');
    this.headers.append('Accept', 'application/json');
  }

  getDocsRestful(){
    let _top10Url:string = 'http://localhost:8000/top10';
    return this._http.get(_top10Url)
                    .map(res => res.json())
                    .catch(this.handleError);
  }

  getDocsRestfulRepeat(){
    console.log('in');
    let _top10Url:string = 'http://localhost:8000/top10';
    return Observable.interval(500)
                    .switchMap(() => this._http.get(_top10Url)
                    .map(res => res.json()))
                    .catch(this.handleError);
  }

  postResAvg(fromDate:string, toDate:string) {
    let _resAvgUrl:string = 'http://localhost:8000/avg-res-time';
    let _toParam = JSON.stringify({ reference_date_from: fromDate,
                                    reference_date_to: toDate})
    return this._http.post(_resAvgUrl, _toParam, { headers: this.headers})
                    .map(res => res.json())
                    .catch(this.handleError)
  }

  getEvents(){
    let _top10Url:string = 'http://localhost:8000/avg-res-time';
    return this._http.get(_top10Url)
                    .map(res => res.json())
                    .catch(this.handleError);
  }

  getAvgResTime(){
    let _avgResTimeUrl:string = 'http://localhost:8000/avg-res-time';
    return this._http.get(_avgResTimeUrl)
                    .map(res => res.json())
                    .catch(this.handleError);
  }

  private handleError (error: Response) {
    console.error(error)
    return Observable.throw(error.json() || 'error')
  }
}
