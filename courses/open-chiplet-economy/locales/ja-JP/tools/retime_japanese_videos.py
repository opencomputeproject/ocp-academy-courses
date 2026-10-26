"""Map the approved English storyboard clock to measured Japanese speech anchors."""
from pathlib import Path
import importlib,json,sys,wave,bisect
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from tools.japanese_video_audio import approved_timing
COURSE=json.loads((ROOT/'course.json').read_text())
ANCHORS={
'm1':[(0,None),(4.44,'企業を結び付けています'),(7.86,'活動は'),(10.5,'ツールとフローは'),(13.78,'エコシステムの標準は'),(16.76,'オープンインターフェースは'),(19.6,'ある供給者から'),(20.38,'演算ダイを'),(21.44,'演算ダイを','end'),(22.26,'入出力ダイを'),(23.4,'入出力ダイを','end'),(24.22,'それでも'),(25.62,'パッケージの互換性'),(26.88,'テストアクセス'),(27.84,'起動動作'),(28.94,'商業上の責任'),(30.56,'このプロジェクトは'),(33.78,'仕様のレビュー','start',-.4),(35.0,'仕様のレビュー'),(35.95,'仕様のレビュー','end'),(36.42,'モデルの提供'),(37.25,'モデルの提供','end'),(37.72,'実装のテスト'),(38.6,'実装のテスト','end'),(39.32,'どのような貢献を利用しても')],
'm4':[(0,None),(2.84,'電気的な接続'),(4.1,'電気的な接続','end'),(4.84,'ピン配置'),(5.48,'電圧'),(6.22,'タイミング'),(7.04,'チャネル'),(7.94,'互換性が必要'),(9.04,'リンク層'),(12.26,'方式によって'),(14.16,'フレーミング'),(14.78,'エラー保護'),(15.84,'フロー制御'),(16.94,'プロトコルは'),(19.8,'例えば'),(19.88,'メモリの読み出し要求'),(22.04,'同じように解釈'),(24.56,'プロトコルアダプターで'),(25.8,'チップ内のバスを'),(26.72,'ダイ間の転送方式に'),(27.36,'対応付ける'),(27.52,'こともできます'),(29.16,'したがって'),(29.24,'電気的な接続の成功'),(31.6,'十分ではありません'),(33.06,'初期化','start',-.65),(34.24,'初期化','start',-.15),(37.8,'初期化'),(38.96,'エラー時')],
'm5':[(0,None),(4.54,'その段階での機能や電気的な動作'),(8.02,'高価な組立の前には'),(9.5,'追加のダイレベル選別'),(12.2,'パッケージ基板の検査は'),(15.76,'パッケージ基板とシリコンウエハーは'),(19.36,'組立後には'),(20.34,'新しい接続'),(21.24,'新しい接続','end'),(23.28,'パッケージ試験で'),(28.0,'システム試験で'),(28.1,'実際の動作条件'),(29.4,'実際の動作条件に近い','end'),(30.0,'統合動作'),(31.26,'統合動作を調べます','end'),(32.82,'各段階は互いを補います'),(34.78,'ウエハー選別の合格が'),(37.66,'最終システム試験が')],
'm9':[(0,None),(3.24,'合意したシミュレーション要求を'),(5.86,'供給者のモデルへ届けます','end'),(9.38,'境界条件を交換し'),(10.2,'境界条件を','start',.1),(11.74,'交換し','end'),(11.86,'許可された結果を'),(13.38,'結果を受け取る','end'),(17.08,'安全なコンテナだけでは足りません'),(19.76,'モデルの識別と版'),(21.38,'利用権限'),(23.18,'許可する出力'),(27.42,'サミットの提案は'),(30.2,'初期の概念実証の方向性です','end'),(33.24,'学ぶべき点は'),(38.34,'精度と機密性の両方に'),(41.36,'明示的な方針と根拠')]
}
DURATIONS={'m1':43.748662131519275,'m4':39.52285714285714,'m5':41.65963718820862,'m9':42.67954648526077}
SLIDES={'m1':(1,3),'m4':(4,3),'m5':(5,3),'m9':(9,6)}
output={}
for name,rows in ANCHORS.items():
    module,slide=SLIDES[name];s=COURSE['modules'][module-1]['slides'][slide-1]
    raw=json.loads((ROOT/f'_narration_work/alignments/narration-m{module}s{slide}.json').read_text())['transcription']
    aligned=approved_timing(raw,s['transcript']);words=aligned['words'];whole=''.join(w['text'] for w in words)
    with wave.open(str(ROOT/s['audio']['wav_file'])) as wav:duration=wav.getnframes()/wav.getframerate()
    mapped=[]
    for row in rows:
        old,phrase=row[:2]
        if phrase is None:time=0
        else:
            index=whole.index(phrase);mode=row[2] if len(row)>2 else 'start';offset=row[3] if len(row)>3 else 0
            time=words[index+len(phrase)-1]['end'] if mode=='end' else words[index]['start'];time+=offset
        mapped.append({'english_seconds':old,'japanese_seconds':round(time,5),'phrase':phrase})
    mapped.append({'english_seconds':DURATIONS[name],'japanese_seconds':duration,'phrase':'end'})
    for a,b in zip(mapped,mapped[1:]):
        if b['japanese_seconds']<=a['japanese_seconds']:raise ValueError(f'{name}: nonmonotonic anchors: {a} -> {b}')
    output[name]={'duration_seconds':duration,'source_duration_seconds':DURATIONS[name],
                  'recognition_similarity':aligned['recognition_similarity'],'anchors':mapped}
    print(name,round(duration,3),'seconds;',len(mapped),'reviewable speech anchors')
(ROOT/'video_source/timing-ja.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
