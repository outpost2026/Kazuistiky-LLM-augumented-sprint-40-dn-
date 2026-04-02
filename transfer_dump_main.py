import functions_framework
from flask import jsonify
import traceback

import material_scraper
import notebook_scraper
import notebook_deepdive
import meteo_miner

@functions_framework.http
def run_orchestrator(request):
    """
    Vstupní bod pro Cloud Function.
    Očekává JSON payload, např.: {"target": "meteo"}
    Povolené targety: 'material', 'notebooky', 'notebooky_deep', 'meteo'
    """
    request_json = request.get_json(silent=True)

    if not request_json or 'target' not in request_json:
        return jsonify({"error": "Chybí povinný parametr 'target' v JSON payloadu."}), 400

    target = request_json['target']
    print(f"[*] ORCHESTRÁTOR: Zachycen požadavek pro těžbu -> {target}")

    try:
        if target == "material":
            material_scraper.run_pipeline()
            return jsonify({"status": "Těžba materiálu úspěšně dokončena."}), 200

        elif target == "notebooky":
            notebook_scraper.run_pipeline()
            return jsonify({"status": "Těžba notebooků úspěšně dokončena."}), 200

        elif target == "notebooky_deep":
            notebook_deepdive.run_deepdive()
            return jsonify({"status": "Těžba notebooků detail úspěšně dokončena."}), 200

        elif target == "meteo":
            meteo_miner.run_pipeline()
            return jsonify({"status": "Těžba meteo dat úspěšně dokončena."}), 200

        else:
            return jsonify({
                "error": f"Neznámý cíl: {target}. Povolené hodnoty: 'material', 'notebooky', 'notebooky_deep', 'meteo'."
            }), 400

    except Exception as e:
        error_msg = f"Kritická chyba v modulu {target}:\n{str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return jsonify({"error": "Vnitřní chyba skriptu. Zkontrolujte GCP Logs."}), 500
