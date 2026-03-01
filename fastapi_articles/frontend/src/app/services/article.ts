import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Article {
  id: number;
  nom: string;
  description: string;
  prix: number;
  en_stock: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class ArticleService {

  private apiUrl = 'http://127.0.0.1:8000/articles';

  constructor(private http: HttpClient) {}

  getArticles(): Observable<Article[]> {
    return this.http.get<Article[]>(`${this.apiUrl}/`);
  }

  addArticle(article: Article): Observable<Article> {
    return this.http.post<Article>(`${this.apiUrl}/`, article);
  }

  deleteArticle(id: number) {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}