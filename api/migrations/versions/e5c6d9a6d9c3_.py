"""empty message

Revision ID: e5c6d9a6d9c3
Revises: 53d13c2cdac7
Create Date: 2022-03-17 21:10:46.722438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5c6d9a6d9c3'
down_revision = '53d13c2cdac7'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_alerts():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_alerts():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_blockchains():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_blockchains():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_challenges():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_challenges():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_connections():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_connections():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_drives():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('drives',
    sa.Column('serial_number', sa.String(), nullable=False),
    sa.Column('hostname', sa.String(length=255), nullable=False),
    sa.Column('blockchain', sa.String(length=64), nullable=False),
    sa.Column('model_family', sa.String(), nullable=True),
    sa.Column('device_model', sa.String(), nullable=True),
    sa.Column('device', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('temperature', sa.REAL(), nullable=True),
    sa.Column('power_on_hours', sa.REAL(), nullable=True),
    sa.Column('size_gibs', sa.REAL(), nullable=True),
    sa.Column('capacity', sa.String(), nullable=True),
    sa.Column('smart_info', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('serial_number')
    )
    # ### end Alembic commands ###


def downgrade_drives():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('drives')
    # ### end Alembic commands ###


def upgrade_farms():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_farms():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_keys():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_keys():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_partials():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_partials():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_plotnfts():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_plotnfts():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_plottings():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_plottings():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_plots():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_plots():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_pools():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_pools():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_wallets():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_wallets():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_workers():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_workers():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_stat_plot_count():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_stat_plot_count():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_stat_plots_size():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_stat_plots_size():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_stat_total_coins():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_stat_total_coins():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_stat_netspace_size():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_stat_netspace_size():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_stat_time_to_win():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_stat_time_to_win():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_stat_plots_total_used():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_stat_plots_total_used():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_stat_plots_disk_used():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_stat_plots_disk_used():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_stat_plots_disk_free():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_stat_plots_disk_free():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_stat_plotting_total_used():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_stat_plotting_total_used():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_stat_plotting_disk_used():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_stat_plotting_disk_used():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_stat_plotting_disk_free():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_stat_plotting_disk_free():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

def upgrade_stat_farmed_blocks():
    pass

def downgrade_stat_farmed_blocks():
    pass

def upgrade_stat_wallet_balances():
    pass

def downgrade_stat_wallet_balances():
    pass

def upgrade_stat_total_balance():
    pass

def downgrade_stat_total_balance():
    pass

def upgrade_stat_effort():
    pass

def downgrade_stat_effort():
    pass

def upgrade_warnings():
    pass

def downgrade_warnings():
    pass

def upgrade_stat_container_mem_gib():
    pass

def downgrade_stat_container_mem_gib():
    pass

def upgrade_stat_host_mem_pct():
    pass

def downgrade_stat_host_mem_pct():
    pass

def upgrade_transfers():
    pass

def downgrade_transfers():
    pass