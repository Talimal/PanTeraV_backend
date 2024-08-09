from flask import Blueprint, request
import api

bp = Blueprint("tali", __name__, "/")

# ########################################################################################################################################################################
# Tali's server
###################################################################################################################################################################################


def call_tali_preprocess():
    api.initialize()


@bp.route("/initialize_tali", methods=["POST"])
def set_dataset_name():
    call_tali_preprocess()
    return ""  # every route method has to return something"


@bp.route("/get_symbol_TIRPs")
def get_symbol_TIRPs():
    return api.get_symbol_TIRPs()


@bp.route("/tirpsJson")
def get_tirps_json():
    return api.get_tirps_json()


@bp.route("/symbols_to_names")
def get_symbols_names():
    return api.get_symbols_names()