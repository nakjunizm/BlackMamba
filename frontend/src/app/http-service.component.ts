import {Injectable} from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import './rxjs-operators';

@Injectable()
export class HttpService {

  constructor(private _http: Http){}

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

  private handleError (error: Response) {
    console.error(error)
    return Observable.throw(error.json() || 'error')
  }
}
