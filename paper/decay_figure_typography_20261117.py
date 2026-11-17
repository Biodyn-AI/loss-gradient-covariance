"""JOTA-only decay-response typography from the frozen recorded summary.

No confidence intervals, fitted quantities or new statistics are computed.
Pass --scientific-root to locate results/ and experiments/ in another copy.
LaTeX uses the supplied figure assets and does not execute this producer.
The local decay_figure_typography_before_20261117/ backup is not for release.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/"data"/"workspace"
HELPER_SHA="e53dc967b179d61628e44c35b8780d2a211648e5e517552d2dad7f31f37941cd"
helper_path=HERE/"figure_typography_20261117.py"
assert hashlib.sha256(helper_path.read_bytes()).hexdigest()==HELPER_SHA
spec=importlib.util.spec_from_file_location("jota_typography_helper",helper_path)
helper=importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
PINS={
 "results/q2_decay_contrast_analysis_20261117/run/summary.json":"db1802a09c53214dc21e62f53829b7a1b9afb140ca717de83a04149aba3e201a",
 "experiments/q2_phase_paper_figures_20261117.py":"9ff88d7c24ee3fa6710c13cb134ee35b44458b51bee77492ad968991e45d6e0f",
}

def decay_figure(rows):
    assert len(rows)==2
    prediction=rows[0]["response_contrast_per_delta"]
    assert all(row["response_contrast_per_delta"]==prediction for row in rows)
    band=[float(prediction[k]) for k in ("lower","upper")]
    eta=np.array([row["runtime_delta"] for row in rows])
    point=np.array([row["contrast_per_delta"] for row in rows])
    intervals=np.array([row["simultaneous_95_per_delta"] for row in rows])
    assert np.isfinite(eta).all() and np.isfinite(point).all() and np.isfinite(intervals).all()
    # The LaTeX figure is 0.95 linewidth: 8.5 pt here becomes 8.075 pt there.
    style={"font.size":8.5,"axes.titlesize":8.5,"axes.labelsize":8.5,
           "xtick.labelsize":8.5,"ytick.labelsize":8.5,"legend.fontsize":8.5}
    with helper.plt.rc_context(style):
        fig,axis=helper.plt.subplots(figsize=(helper.WIDTH,helper.WIDTH*3.5/7.2))
        fig.subplots_adjust(left=.19,right=.96,bottom=.22,top=.87)
        axis.axhspan(*band,color="#617b96",alpha=.20,
                     label="Independent response (unknown remainder)")
        axis.axhline(0,color="#777777",linestyle="--",linewidth=.8,label="Leading contrast")
        # Endpoint subtraction is only Matplotlib's plotting convention;
        # every recorded mean and interval endpoint remains unchanged.
        axis.errorbar(eta,point,yerr=np.stack((point-intervals[:,0],intervals[:,1]-point)),
                      color="#b63c39",marker="o",markersize=3,linestyle="none",capsize=2,
                      linewidth=.9,label="Native contrast (approx. simultaneous 95%)")
        for x,y,row in zip(eta,point,rows):
            rightmost=x==max(eta)
            axis.annotate("n="+str(row["n"]),(x,y),xytext=(-4 if rightmost else 4,5),
                          ha="right" if rightmost else "left",textcoords="offset points",fontsize=8.5)
        axis.set(xlabel=r"Response scale $\delta=r^{1-\gamma}$",
                 ylabel=r"$(\mathbb{E}_{\rm high}Y^2-\mathbb{E}_{\rm low}Y^2)/\delta$",
                 title="Test after cancelling the shared leading level")
        axis.tick_params(labelsize=8.5,pad=2,length=2)
        axis.grid(alpha=.15)
        axis.legend(loc="upper center",frameon=True,facecolor="white",edgecolor="none",
                    framealpha=1,fontsize=8.5,labelspacing=.3,borderpad=.2,
                    handlelength=1.4,handletextpad=.4)
    return fig,axis

def run(scientific_root=ROOT):
    root=Path(scientific_root).resolve()
    assert all(helper.sha(root/name)==digest for name,digest in PINS.items())
    saved=json.loads((root/"results/q2_decay_contrast_analysis_20261117/run/summary.json").read_text())
    assert saved["analysis_complete"]
    fig,axis=decay_figure(saved["zero_start_final_window_table"])
    helper.assert_fonts_and_bounds(fig)
    output=HERE/"figures"
    backup=HERE/"decay_figure_typography_before_20261117"
    receipt=HERE/"decay_figure_typography_provenance_20261117.json"
    assert not backup.exists() and not receipt.exists(),"one execution only; retain prior provenance"
    backup.mkdir()
    previous={}
    for extension in ("pdf","svg","png"):
        path=output/("decay_contrast."+extension)
        if path.exists():
            previous[path.name]=helper.sha(path)
            shutil.copyfile(path,backup/path.name)
            assert helper.sha(backup/path.name)==previous[path.name]
    fig.savefig(output/"decay_contrast.pdf",metadata={"CreationDate":None,"ModDate":None})
    fig.savefig(output/"decay_contrast.svg",metadata={"Date":None})
    fig.savefig(output/"decay_contrast.png")
    helper.plt.close(fig)
    assert all(helper.sha(root/name)==digest for name,digest in PINS.items())
    report={"status":"complete","source_sha256":helper.sha(Path(__file__)),
        "helper_source_sha256":HELPER_SHA,
        "test_source_sha256":helper.sha(HERE/"test_decay_figure_typography_20261117.py"),
        "input_sha256_before":PINS,"input_sha256_after":{name:helper.sha(root/name) for name in PINS},
        "scientific_inputs_unchanged":True,"scientific_random_draws":0,"fitted_parameters":0,
        "new_scientific_statistics":0,"final_width_cm":11.9,"minimum_normal_font_pt":8.5,
        "actual_font_at_95_percent_linewidth_pt":8.075,"aspect_ratio":"7.2:3.5",
        "recorded_display":saved["zero_start_final_window_table"],
        "interval_scope":"Unchanged: approximate simultaneous 95% native contrasts; independently frozen response-functional interval, with unknown finite-rate remainder and equilibration error excluded.",
        "prior_jota_asset_directory":backup.name,"prior_jota_asset_sha256":previous,
        "artifacts":{path.name:{"bytes":path.stat().st_size,"sha256":helper.sha(path)}
                     for path in [output/("decay_contrast."+ext) for ext in ("pdf","svg","png")]}}
    with receipt.open("x") as stream:json.dump(report,stream,indent=2);stream.write("\n")
    print(json.dumps({"status":"complete","normal_font_at_95_percent_linewidth_pt":8.075,"inputs_unchanged":True}))

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scientific-root",type=Path,default=ROOT)
    run(parser.parse_args().scientific_root)
