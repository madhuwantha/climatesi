import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'client';

  public base64 = "";

  constructor(
    public http: HttpClient,
  ){
  }
  ngOnInit(): void {
    this.http.get<any>('http://127.0.0.1:3000/api/mac')
    .subscribe(r => {
      this.base64 = 'data:image/jpg;base64,'+r.data;
    })
  }


}
