import seaborn as sns
import pandas as pd


def K(logs_file_path: str, n_epochs: int):
    log_data = open(logs_file_path, 'r')
    df = {"type": [], "epoch": [], "loss": []}

    for line in log_data:
        columns = line.split(' ')
        if len(columns) == 15:
            df["type"].append(columns[3])
            df["epoch"].append(int(columns[6]))
            df["loss"].append(float(columns[14][:6]))

    df = pd.DataFrame(df)

    train_df = df[df.type == "Train"]
    val_df = df[df.type == "Valid"]

    training_loss = list(train_df.groupby("epoch").mean().loss)[:n_epochs]
    validation_loss = list(val_df.groupby("epoch").mean().loss)[:n_epochs]

    epoch_n = list(range(n_epochs)) + list(range(n_epochs))
    labels = ["train" for _ in range(n_epochs)] + ["validation" for _ in range(n_epochs)]
    loss = training_loss + validation_loss

    assert len(epoch_n) == len(loss) == len(labels), "Data Frame can't be created"

    plot_df = pd.DataFrame({"epoch": epoch_n, "label": labels, "loss": loss})

    sns.lineplot(data=plot_df, x="epoch", y="loss", hue="label")
