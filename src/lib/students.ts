// 「数字で見る都市大の現状」用の学生数データ(src/data/students.csv)を読み込む。
// 比率の列(男女比・留学生比)は使わず、人数から計算し直す。
import raw from '../data/students.csv?raw';

export type CampusKey = 'all' | 'sc' | 'yc';

export interface Counts {
  total: number;
  male: number;
  female: number;
  intl: number;
}

export interface YearRow {
  year: number;
  all: Counts;
  sc: Counts;
  yc: Counts;
}

export const campusLabels: Record<CampusKey, string> = {
  all: '全学',
  sc: '世田谷キャンパス',
  yc: '横浜キャンパス',
};

// CSV の列名(キャンパスごと)。表記ゆれ(「SC男子学生」と「YC男子学生数」)はここで吸収する。
const columns: Record<CampusKey, Record<keyof Counts, string[]>> = {
  all: { total: ['全学生総数'], male: ['男子学生数'], female: ['女子学生数'], intl: ['留学生数'] },
  sc: { total: ['SC全学生総数'], male: ['SC男子学生数', 'SC男子学生'], female: ['SC女子学生数', 'SC女子学生'], intl: ['SC留学生数'] },
  yc: { total: ['YC全学生総数'], male: ['YC男子学生数', 'YC男子学生'], female: ['YC女子学生数', 'YC女子学生'], intl: ['YC留学生数'] },
};

function parse(text: string): YearRow[] {
  const lines = text.replace(/^﻿/, '').split(/\r?\n/).filter((l) => l.trim() !== '');
  const header = lines[0].split(',').map((h) => h.trim());
  const indexOf = (names: string[]) => {
    const i = header.findIndex((h) => names.includes(h));
    if (i < 0) throw new Error(`students.csv: 列「${names[0]}」が見つかりません`);
    return i;
  };

  return lines.slice(1).map((line) => {
    const cells = line.split(',').map((c) => c.trim());
    const year = Number(cells[0]);
    if (!Number.isInteger(year)) throw new Error(`students.csv: 年度が読めません: ${line}`);
    const num = (names: string[]) => {
      const v = Number(cells[indexOf(names)].replace(/[^\d.-]/g, ''));
      if (!Number.isFinite(v)) throw new Error(`students.csv: ${year}年の「${names[0]}」が数値ではありません`);
      return v;
    };
    const counts = (k: CampusKey): Counts => ({
      total: num(columns[k].total),
      male: num(columns[k].male),
      female: num(columns[k].female),
      intl: num(columns[k].intl),
    });
    const row: YearRow = { year, all: counts('all'), sc: counts('sc'), yc: counts('yc') };

    // 入力ミスをビルド時に検出する
    for (const k of ['all', 'sc', 'yc'] as CampusKey[]) {
      const c = row[k];
      if (c.male + c.female !== c.total) {
        throw new Error(`students.csv: ${year}年 ${campusLabels[k]}の男子+女子(${c.male + c.female})が総数(${c.total})と一致しません`);
      }
    }
    if (row.sc.total + row.yc.total !== row.all.total) {
      throw new Error(`students.csv: ${year}年 世田谷+横浜(${row.sc.total + row.yc.total})が全学(${row.all.total})と一致しません`);
    }
    return row;
  }).sort((a, b) => a.year - b.year);
}

export const students: YearRow[] = parse(raw);
