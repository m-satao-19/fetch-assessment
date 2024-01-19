from flask import Flask, jsonify, Response, request
from functools import wraps
import uuid
import json
import logging

from utils import calculate_points

RECEIPTS = "receipts.json"
LOGS = 'logs.log'

def create_app():

    app = Flask("fetch")
    logging.basicConfig(filename=LOGS, level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    logger = logging.getLogger("fetch")

    def required_params(*args):

        required = list(args)

        def decorator(fn):

            @wraps(fn)
            def wrapper(*args,**kwargs):
                missing = [param for param in required if param not in request.json]

                if missing:
                    app.logger.error("Missing keys in request body. Returning error")
                    return jsonify({"msg": "Missing keys in request body"}),400
                
                return fn(*args,**kwargs)
            
            return wrapper
        
        return decorator
    

    @app.route('/')
    def base():
        app.logger.info("App accessed")
        return "Fetch Backend Developer Assessment"
    
    
    @app.route('/receipts/process',methods=['POST'])
    @required_params("retailer","purchaseDate","purchaseTime","items","total")
    def process_receipt():

        receipt_id = str(uuid.uuid4())
        
        try:
            with open(RECEIPTS) as f:
                receipt_list = json.load(f)

        except FileNotFoundError as e:
            app.logger.warn("JSON file not found. Creating a new JSON file")
            receipt_list = {}
        
        receipt_list[receipt_id] = request.json
        
        with open(RECEIPTS,'w') as f:
            json.dump(receipt_list,f)

        app.logger.info(f"Receipt with id:{receipt_id} added")

        return jsonify({'id':receipt_id}),201
    

    @app.route('/receipts/<id>/points',methods=['GET'])
    def get_points(id):

        try:
            with open(RECEIPTS) as f:
                receipt_list = json.load(f)

            receipt = receipt_list[id]
            
        except Exception as e:
            app.logger.error("Receipt id not found. Returning error")
            return jsonify({"msg": "Receipt id not found"}),400
        
        app.logger.info(f"Calculating points for receipt id:{id}")
        
        points = calculate_points(receipt=receipt)

        return jsonify({'points':points}),200

    return app