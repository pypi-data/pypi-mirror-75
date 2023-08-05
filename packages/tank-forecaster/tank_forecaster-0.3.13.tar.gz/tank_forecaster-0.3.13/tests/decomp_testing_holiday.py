# set up bar plot
holidays = decomp[2]
holiday_factors = holidays.iloc[[0, 146, 184, 246, 326, 360]]
holiday_names = pd.Series(['New Years', 'Memorial Day', '4 July',
                 'Labor Day', 'Thanks', 'Xmas'])
holiday_factors.reset_index(drop=True, inplace=True)


plt.close()
sns.set_palette(sns.color_palette("muted", 6))
fig = sns.barplot(y=holiday_factors, x=holiday_names).set_title(f'KT{store}: Fuel type {tank_type}')
plt.savefig(fname=f'../figures/gam_decomp/KT{store}{tank}_holiday_factor.png')
plt.show()


# plt.close()
# sns.set()
# fig, axs = plt.subplots(2)
# fig = sns.lineplot(y=generic_weekly_decomp, x=range(len(generic_weekly_decomp)), ax=axs[1])
# fig = sns.lineplot(y=generic_yearly_decomp, x=range(len(generic_yearly_decomp)), ax=axs[0]).set_title('Generic Seasonal Decomposition based on UNL 87')
# plt.savefig(fname=f'../figures/decompose/generic_seasonal_decomp.png')
# plt.show()
