"""
웹 대시보드
"""
from flask import Flask, render_template, jsonify
from storage import Database
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    """메인 대시보드"""
    return render_template('dashboard.html')

@app.route('/api/products')
def get_products():
    """모든 상품 조회"""
    with Database() as db:
        products = db.get_all_products()
        
        result = []
        for product in products:
            result.append({
                'id': product.id,
                'name': product.name,
                'url': product.url,
                'current_price': product.price,
                'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': product.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify(result)

@app.route('/api/price-history/<int:product_id>')
def get_price_history(product_id):
    """상품 가격 변동 이력"""
    with Database() as db:
        from storage.models import PriceHistory
        
        history = db.session.query(PriceHistory)\
            .filter_by(product_id=product_id)\
            .order_by(PriceHistory.recorded_at)\
            .all()
        
        result = []
        for record in history:
            result.append({
                'price': record.price,
                'recorded_at': record.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify(result)

@app.route('/api/stats')
def get_stats():
    """통계 정보"""
    with Database() as db:
        products = db.get_all_products()
        
        total_products = len(products)
        
        # 최근 24시간 내 가격 변동
        from storage.models import PriceHistory
        yesterday = datetime.now() - timedelta(days=1)
        recent_changes = db.session.query(PriceHistory)\
            .filter(PriceHistory.recorded_at >= yesterday)\
            .count()
        
        return jsonify({
            'total_products': total_products,
            'recent_changes': recent_changes
        })

def run_dashboard(port=5000):
    """대시보드 실행"""
    print(f"""
    
🌐 웹 대시보드가 실행되었습니다!
    
📊 대시보드: http://localhost:{port}
    
종료하려면 Ctrl+C를 누르세요
    """)
    
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    run_dashboard()