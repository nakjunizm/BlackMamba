export interface ReqEvent {
  id:string;
  type:string;
  accesslogId:string;
  requestUri:string;
  requestMethod:string;
  responseTime:string;
  responseCode:string;
  isChecked:boolean;
}