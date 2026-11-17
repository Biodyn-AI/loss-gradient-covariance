"""JOTA-only typography repair from exact saved observations; no RNG or fitting.

The original scientific producers and assets are read-only. At 11.9 cm final
width, all normal labels use at least 8 points. Original aspect ratios are
retained. This program only extracts the original declared display subset;
it neither recomputes confidence intervals nor estimates a new statistic.

Portability: pass --scientific-root /path/to/scientific/archive to locate the
pinned results/ and experiments/ trees. LaTeX compilation uses the supplied
figure files and does not execute this producer. Regeneration is protected
against overwriting an existing provenance receipt; use a fresh source copy.
The local figure_typography_before_20261117/ backup is not a public artifact.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text
from matplotlib.ticker import LogLocator, NullFormatter
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/"data"/"workspace"
WIDTH=11.9/2.54
PINS={
 "results/q2_matrix_analysis_20261117/run/summary.json":"93bfb6d29724b8a73bae260eb1627258313f14c744bce7897a2aee4843e33148",
 "results/q2_matrix_validation_20261117/run/summary.json":"33fff2e3897f3bd9be0134e34e98bb890b35e98eb2b45fd30809e8c738a12a17",
 "results/q2_quadratic_analysis_20261116/run/summary.json":"2cacd0b19a00c04cf2c3909f848023ca6e9923113bc7ceccf90d9431cda5499c",
 "results/q2_matrix_validation_20261117/run/samples_and_terminal.npz":"f1df66757c55324655df8eb9d4139ce28740742ad937ad835134bf5f57ec2115",
 "experiments/q2_phase_paper_figures_20261117.py":"9ff88d7c24ee3fa6710c13cb134ee35b44458b51bee77492ad968991e45d6e0f",
 "experiments/q2_stationary_figures.py":"702cac53e79a11f6148c5f72b0db1e68a2e303bbd22ca8d069312976a62bb888",
}
STYLES=[("AdamW","independent","#1767a6","o","-"),
        ("AdamW","coupled","#b63c39","D","-"),
        ("SGD","independent","#414141","s","--"),
        ("SGD","coupled","#949494","+",":")]
plt.rcParams.update({"font.size":8,"axes.titlesize":8,"axes.labelsize":8,
 "xtick.labelsize":8,"ytick.labelsize":8,"legend.fontsize":8,
 "axes.spines.top":False,"axes.spines.right":False,"savefig.dpi":300,
 "svg.fonttype":"none","svg.hashsalt":"jota-typography-20261117",
 "pdf.fonttype":42,"ps.fonttype":42})

def sha(path):
    digest=hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b""):
            digest.update(chunk)
    return digest.hexdigest()

def risk_series(table,method,law,value_key,interval_key):
    assert len(table)==3
    eta=np.array([row["eta"] for row in table])
    point=np.array([row["methods"][method][law][value_key] for row in table])
    band=np.array([row["methods"][method][law][interval_key] for row in table])
    assert eta.shape==(3,) and point.shape==(3,) and band.shape==(3,2)
    assert np.isfinite(eta).all() and np.isfinite(point).all() and np.isfinite(band).all()
    return eta,point,band

def error_bar(axis,eta,point,band,**style):
    # Identical interval endpoints to the old producer. Subtraction only
    # converts the saved endpoints to Matplotlib's distance convention.
    axis.errorbar(eta,point,yerr=np.maximum(0,np.stack((point-band[:,0],band[:,1]-point))),
                  capsize=2,markersize=3,linewidth=.9,elinewidth=.8,**style)

def log_ticks(axis):
    axis.xaxis.set_major_locator(LogLocator(base=10,numticks=3))
    axis.xaxis.set_minor_formatter(NullFormatter())
    axis.tick_params(which="both",pad=2,length=2)

def matrix_figure(table,clouds):
    assert len(clouds)==4 and all(c.shape==(2,256) and np.isfinite(c).all() for c in clouds)
    fig,axes=plt.subplots(1,2,figsize=(WIDTH,WIDTH*4.1/9))
    fig.subplots_adjust(left=.15,right=.985,bottom=.2,top=.88,wspace=.49)
    for method,law,color,marker,line in STYLES:
        eta,point,band=risk_series(table,method,law,"risk","simultaneous_95")
        assert (band[:,0]>0).all()
        error_bar(axes[0],eta,point,band,color=color,marker=marker,linestyle=line,
                  label=method+": "+("indep." if law=="independent" else "coupled"),
                  zorder=4 if method=="AdamW" else 3)
    axes[0].set(xscale="log",yscale="log",xlabel=r"Step size $\eta$",
                ylabel="Excess risk",title="Stationary error")
    axes[0].grid(alpha=.18,which="both")
    axes[0].legend(frameon=False,loc="center left",borderpad=.1,labelspacing=.2,
                   handlelength=1.25,handletextpad=.35)
    log_ticks(axes[0])
    maximum=max(float(np.abs(cloud).max()) for cloud in clouds)*1.1
    for cloud,(_,_,color,marker,_) in zip(clouds,STYLES):
        axes[1].scatter(*cloud,s=3,alpha=.45,color=color,marker=marker,rasterized=False,linewidths=.4)
    axes[1].plot([-maximum,maximum],[maximum,-maximum],color="#888888",linewidth=.55,linestyle=":",zorder=0)
    axes[1].axhline(0,color="#aaaaaa",linewidth=.45)
    axes[1].axvline(0,color="#aaaaaa",linewidth=.45)
    axes[1].set(xlabel=r"$u_1$",ylabel=r"$u_2$",title=r"States: $\eta=4\cdot10^{-5}$",
                xlim=(-maximum,maximum),ylim=(-maximum,maximum),aspect="equal")
    axes[1].grid(alpha=.12)
    axes[1].tick_params(pad=2,length=2)
    # This upper-right region contains neither terminal well. No samples are
    # dropped: four full clouds remain on the main axes, three in the inset.
    inset=axes[1].inset_axes([.55,.63,.4,.33])
    for index in (0,2,3):
        inset.scatter(*clouds[index],s=1,alpha=.5,color=STYLES[index][2],rasterized=False,linewidths=0)
    inset.set(xlim=(-.012,.012),ylim=(-.012,.012),xticks=[-.01,.01],yticks=[-.01,.01],
              xticklabels=["−.01",".01"],yticklabels=["−.01",".01"],title="Near 0")
    inset.tick_params(labelsize=8,length=1.5,pad=1)
    inset.set_title("Near 0",fontsize=8,pad=2)
    return fig,axes,inset

def scalar_figure(table,oracle):
    fig,axes=plt.subplots(1,2,figsize=(WIDTH,WIDTH*4.2/10))
    fig.subplots_adjust(left=.12,right=.95,bottom=.22,top=.72,wspace=.62)
    colors={"matching":"#a63e3e","opposite":"#1767a6"}
    for method in ("AdamW","SGD"):
        for law in ("matching","opposite"):
            eta,point,band=risk_series(table,method,law,"risk_per_eta","percentile_95")
            error_bar(axes[0],eta,point,band,label=method+": "+("match" if law=="matching" else "opposite"),
                      color=colors[law],marker="o" if method=="AdamW" else "s",
                      linestyle="-" if method=="AdamW" else ":")
        ratio=[row["methods"][method]["opposite_over_matching"] for row in table]
        point=np.array([row["point"] for row in ratio])
        band=np.array([row["percentile_95"] for row in ratio])
        error_bar(axes[1],eta,point,band,label=method,color="#1767a6" if method=="AdamW" else "#555555",
                  marker="o" if method=="AdamW" else "s")
    def bounds(record): return [float(record[k]) for k in ("lower","upper")]
    for index,law in enumerate(("matching","opposite")):
        axes[0].axhspan(*bounds(oracle["risk_per_eta"][index]),color=colors[law],alpha=.12)
    axes[1].axhspan(*bounds(oracle["anti_over_com_risk"]),color="#1767a6",alpha=.12,label="99% oracle")
    axes[1].axhline(1,color="#555555",linestyle=":",linewidth=.7)
    axes[0].set(xscale="log",xlabel=r"Step size $\eta$",ylabel=r"Risk / $\eta$",title="Risk coefficients")
    axes[1].set(xscale="log",xlabel=r"Step size $\eta$",ylabel="Opp. / matching",title="Pairing ratio")
    for axis in axes:
        axis.grid(alpha=.15)
        log_ticks(axis)
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc="upper center",bbox_to_anchor=(.5,1.01),ncol=2,
               frameon=False,borderpad=.1,labelspacing=.2,columnspacing=1,
               handlelength=1.3,handletextpad=.35)
    axes[1].legend(loc="center",bbox_to_anchor=(.5,.68),frameon=False,borderpad=.1,
                   labelspacing=.2,handlelength=1.25,handletextpad=.35)
    return fig,axes

def drawn_texts(fig):
    # LogLocator also creates off-view tick Text objects. Axis.draw excludes
    # those; include only tick labels whose data coordinate is in view.
    outside=set()
    axes=list(fig.axes)+[child for axis in fig.axes for child in axis.child_axes]
    for axis in axes:
        for dimension,limits,index in ((axis.xaxis,axis.get_xlim(),0),(axis.yaxis,axis.get_ylim(),1)):
            low,high=sorted(limits)
            for tick in dimension.get_major_ticks()+dimension.get_minor_ticks():
                if not low<=tick.get_loc()<=high:
                    outside.update((tick.label1,tick.label2))
    return [text for text in fig.findobj(Text)
            if text not in outside and text.get_visible() and text.get_text()]

def assert_fonts_and_bounds(fig):
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    for text in drawn_texts(fig):
        if text.get_visible() and text.get_text():
            assert text.get_fontsize()>=8
            box=text.get_window_extent(renderer)
            assert box.x0>=-1 and box.x1<=fig.bbox.x1+1,(text.get_text(),"horizontal clipping")
            assert box.y0>=-1 and box.y1<=fig.bbox.y1+1,(text.get_text(),"vertical clipping")

def run(scientific_root=ROOT):
    root=Path(scientific_root).resolve()
    assert all(sha(root/name)==digest for name,digest in PINS.items()),"frozen input mismatch"
    matrix=json.loads((root/"results/q2_matrix_analysis_20261117/run/summary.json").read_text())
    native=json.loads((root/"results/q2_matrix_validation_20261117/run/summary.json").read_text())
    scalar=json.loads((root/"results/q2_quadratic_analysis_20261116/run/summary.json").read_text())
    assert matrix["analysis_complete"] and native["study_complete"] and scalar["analysis_complete"]
    with np.load(root/"results/q2_matrix_validation_20261117/run/samples_and_terminal.npz",allow_pickle=False) as saved:
        state=saved["state"]
        assert state.shape==(12,3,3,2,256)
        clouds=[state[cell,0,0].copy() for cell in (8,9,10,11)]
    prepared=[("matrix_phases",matrix_figure(matrix["zero_start_final_window_table"],clouds)[0]),
              ("scalar_couplings",scalar_figure(scalar["zero_start_final_window_table"],scalar["independent_99_oracle"])[0])]
    for _,fig in prepared: assert_fonts_and_bounds(fig)
    output=HERE/"figures"
    backup=HERE/"figure_typography_before_20261117"
    receipt=HERE/"figure_typography_provenance_20261117.json"
    assert not backup.exists() and not receipt.exists(),"one execution only; retain previous artifacts"
    backup.mkdir()
    before={}
    for name,_ in prepared:
        for extension in ("pdf","svg","png"):
            path=output/(name+"."+extension)
            if path.exists():
                before[path.name]=sha(path)
                shutil.copyfile(path,backup/path.name)
                assert sha(backup/path.name)==before[path.name]
    for name,fig in prepared:
        fig.savefig(output/(name+".pdf"),metadata={"CreationDate":None,"ModDate":None})
        fig.savefig(output/(name+".svg"),metadata={"Date":None})
        fig.savefig(output/(name+".png"))
        plt.close(fig)
    assert all(sha(root/name)==digest for name,digest in PINS.items()),"scientific input changed"
    report={"status":"complete","source_sha256":sha(Path(__file__)),
        "test_source_sha256":sha(HERE/"test_figure_typography_20261117.py"),
        "input_sha256_before":PINS,"input_sha256_after":{name:sha(root/name) for name in PINS},
        "scientific_inputs_unchanged":True,"scientific_random_draws":0,"fitted_parameters":0,
        "new_scientific_statistics":0,"final_width_cm":11.9,"minimum_normal_font_pt":8,
        "aspect_ratios":{"matrix_phases":"9:4.1","scalar_couplings":"10:4.2"},
        "retained_display":{"matrix_risk_curves":4,"matrix_steps_per_curve":3,
            "matrix_terminal_replicas_per_method_coupling":256,"matrix_main_clouds":4,"matrix_inset_clouds":3,
            "scalar_risk_curves":4,"scalar_ratio_curves":2,"scalar_steps_per_curve":3,"scalar_oracle_bands":3},
        "interval_scope":"Unchanged: matrix approximate simultaneous 95%; scalar approximate pointwise 95%; scalar independent oracle 99% joint event.",
        "prior_jota_asset_sha256":before,"prior_jota_asset_directory":backup.name,
        "artifacts":{path.name:{"sha256":sha(path),"bytes":path.stat().st_size}
            for name,_ in prepared for path in (output/(name+"."+extension) for extension in ("pdf","svg","png"))}}
    with receipt.open("x") as stream: json.dump(report,stream,indent=2);stream.write("\n")
    print(json.dumps({"status":report["status"],"minimum_normal_font_pt":8,"input_unchanged":True}))

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scientific-root",type=Path,default=ROOT,
                        help="Root containing the pinned results/ and experiments/ trees; only needed to regenerate figures, not build LaTeX")
    run(parser.parse_args().scientific_root)
