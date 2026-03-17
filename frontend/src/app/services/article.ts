// 📂 src/app/services/article.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// 🔹 exportamos la interfaz Article
export interface Article {
  id: number;
  title: string;
  content: string;
  section: string;
  author: number;
  editor: number | null;
  status: string;
  createdAt: string;
  updatedAt: string;
}

@Injectable({
  providedIn: 'root',
})
export class ArticulosService {
  private apiUrl = 'http://127.0.0.1:8000/article/';

  constructor(private http: HttpClient) {}

  getArticles(): Observable<Article[]> {    
       return this.http.get<Article[]>(this.apiUrl);
  }

  deleteArticle(id: number) {
    return this.http.delete(`${this.apiUrl}${id}`);
  }

  publishArticle(id: number) {
    return this.http.put<Article>(`${this.apiUrl}publish/${id}`, {});
  }

  reviewArticle(id: number) {
    return this.http.put<Article>(`${this.apiUrl}review/${id}`, {});
  }
}